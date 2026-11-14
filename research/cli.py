"""Small explicit CLI. This release intentionally exposes no mass simulation command."""
import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess

from .core import Registry, check_identity, config_hash, historical_seeds, schedule, validate, verify_artifacts
from .native import NativeLab, digest, read, require, rows, write
from .report import benchmark_figure, experiment_report

ROOT=Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.check_output(["git",*args],cwd=ROOT)


def normalized_file(path):
    return Path(path).read_bytes().replace(b"\r\n",b"\n")


def published_registration(config, spec):
    """Prove the contract and analysis were published before execution."""
    p=config["preregistration"]
    commit=p["commit"]
    remote=git("ls-remote","origin","refs/heads/main").decode().split()[0]
    subprocess.run(["git","merge-base","--is-ancestor",commit,remote],cwd=ROOT,check=True,capture_output=True)
    subprocess.run(["git","merge-base","--is-ancestor",commit,"HEAD"],cwd=ROOT,check=True,capture_output=True)
    path=Path(spec).resolve()
    require(ROOT in path.parents, "Spec must be repository-local")
    prior=json.loads(git("show",f"{commit}:{path.relative_to(ROOT).as_posix()}"))
    def intent(value):
        return {k:v for k,v in value.items() if k not in ("status","preregistration")}
    require(intent(prior)==intent(config), "Published experiment contract differs")
    for field in ("document","analysis"):
        relative=Path(p[field])
        target=(ROOT/relative).resolve()
        require(ROOT in target.parents and not relative.is_absolute(), "Unsafe preregistration path")
        blob=git("show",f"{commit}:{relative.as_posix()}")
        require(sha256(blob).hexdigest()==p[field+"_sha256"] and blob==normalized_file(target), "Published document/analysis changed")
    for path in (ROOT/"research").glob("*.py"):
        blob=git("show",f"{commit}:{path.relative_to(ROOT).as_posix()}")
        require(blob==normalized_file(path), "Research code changed since preregistration")


def smoke(args):
    lab=NativeLab(args.runtime,args.game,args.artifacts)
    validation=read(ROOT/"data/valid-002/validation-summary.json")
    check_identity(validation["identity"],lab.identity,validation)
    require(args.artifacts.resolve()!=ROOT and ROOT/"data" not in args.artifacts.resolve().parents,
            "Raw inputs cannot be written under public data/")
    spec=read(ROOT/"research/specs/MECH-000-smoke.json")
    spec["identity"]=lab.identity
    base=lab.baseline()
    # A/A negative control: identical native inputs under two arm labels.
    controls={"baseline":base,"aa_control":deepcopy(base)}
    binaries={}
    for arm,config in controls.items():
        binaries[arm]=args.artifacts.resolve()/(arm+".bin")
        digest_value=lab.encode(config,binaries[arm])
        next(a for a in spec["design"]["arms"] if a["id"]==arm)["setup_sha256"]=digest_value
    commit=git("rev-parse","HEAD").decode().strip()
    spec["status"]="registered"
    spec["preregistration"]=dict(commit=commit,document="docs/PLATFORM.md",analysis="research/stats.py",
        document_sha256=sha256(git("show",f"{commit}:docs/PLATFORM.md")).hexdigest(),
        analysis_sha256=sha256(git("show",f"{commit}:research/stats.py")).hexdigest())
    # Technical A/A only: the parameterized smoke plan is published; no optimization inputs.
    require(spec["stage"]=="technical" and spec["budget"]["max_matches"]==4, "Smoke contract changed")
    remote=git("ls-remote","origin","refs/heads/main").decode().split()[0]
    require(remote==commit, "Publish the complete platform before its native smoke")
    for path in [*ROOT.joinpath("research").glob("*.py"),ROOT/"docs/PLATFORM.md",ROOT/"research/specs/MECH-000-smoke.json"]:
        require(git("show",f"{commit}:{path.relative_to(ROOT).as_posix()}")==normalized_file(path), "Smoke code differs from published version")
    registry=Registry(ROOT/"local/registry")
    receipt=registry.register(spec,ROOT/"data")
    planned=schedule(receipt)
    jobs=[dict(j,config=controls[j["arm"]],binary=binaries[j["arm"]]) for j in planned]
    result,timing=lab.run(jobs,args.artifacts/"matches",workers=2,bounded_validation=True)
    indexed={j["key"]:j for j in planned}
    for r in result:
        j=indexed[r["key"]]
        r.update(scenario=j["scenario"],config_sha256=receipt["config_sha256"])
    by_seed={}
    for r in result:
        by_seed.setdefault(r["seed"],[]).append(r)
    require(all(len(g)==2 and all(g[0][k]==g[1][k] for k in ("score","finish_tick","team_statistics")) for g in by_seed.values()), "A/A negative control mismatch")
    write(args.artifacts/"receipt.json",receipt)
    write(args.artifacts/"results.json",result)
    write(args.artifacts/"summary.json",dict(passed=True,technical_only=True,matches=len(result),
          seed_blocks=len(by_seed),identity=lab.identity,timing=timing,all_aa_exact=True))
    experiment_report(receipt,planned,result,args.artifacts/"report.md")
    print(json.dumps(dict(passed=True,matches=len(result),seed_blocks=len(by_seed))))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest="command",required=True)
    check=commands.add_parser("validate-config")
    check.add_argument("spec",type=Path)
    register=commands.add_parser("register")
    register.add_argument("spec",type=Path)
    register.add_argument("--registry",type=Path,required=True)
    plan=commands.add_parser("plan")
    plan.add_argument("receipt",type=Path)
    watch=commands.add_parser("watch-build")
    watch.add_argument("--game",type=Path,required=True)
    watch.add_argument("--runtime",type=Path)
    watch.add_argument("--check-upstream",action="store_true")
    native=commands.add_parser("smoke")
    for name in ("runtime","game","artifacts"):
        native.add_argument("--"+name,type=Path,required=True)
    plot=commands.add_parser("benchmark-figure")
    plot.add_argument("output",type=Path)
    args=parser.parse_args()
    if args.command=="validate-config":
        raw=read(args.spec)
        c=validate(raw,executable=raw.get("status")=="registered")
        print(json.dumps(dict(valid=True,status=c["status"],experiment_id=c["experiment_id"],executable=c["status"]=="registered")))
    elif args.command=="register":
        c=validate(read(args.spec),executable=True)
        published_registration(c,args.spec)
        print(json.dumps(Registry(args.registry).register(c,ROOT/"data")))
    elif args.command=="plan":
        print(json.dumps(schedule(read(args.receipt)),indent=2))
    elif args.command=="watch-build":
        expected=read(ROOT/"data/valid-002/validation-summary.json")["identity"]
        actual=digest(args.game/"fm_Data/Plugins/x86_64/game_plugin.dll")
        result=dict(actual_engine_sha256=actual,expected_engine_sha256=expected["engine_sha256"],
                    revalidation_required=actual!=expected["engine_sha256"])
        if args.runtime:
            result["actual_host_sha256"]=digest(args.runtime/"engine/fm27_native/FM27Simulator.exe")
            result["actual_fixture_sha256"]=digest(args.runtime/"engine/fm27_native/fixtures/match.pkm")
            result["revalidation_required"] |= (result["actual_host_sha256"]!=expected["adapter_host_sha256"] or
                                                result["actual_fixture_sha256"]!=expected["fixture_sha256"])
        if args.check_upstream:
            output=subprocess.check_output(["git","ls-remote","--tags","https://github.com/lqf0624/fm-tactics-lab.git"],text=True)
            import re
            tags=[line.split("refs/tags/")[-1] for line in output.splitlines() if re.search(r"refs/tags/v[0-9.]+$",line)]
            latest=max(tags,key=lambda tag:tuple(int(n) for n in tag[1:].split(".")))
            result.update(latest_upstream_tag=latest,upstream_review_required=latest!=expected["lab_version"])
        print(json.dumps(result))
        if result["revalidation_required"]:
            raise SystemExit(2)
    elif args.command=="smoke":
        smoke(args)
    else:
        benchmark_figure(read(ROOT/"data/valid-002/validation-summary.json"),args.output)


if __name__=="__main__":
    main()
