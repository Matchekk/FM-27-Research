"""Thin, strict boundary around the separately installed Windows Tactics Lab."""
from copy import deepcopy
from hashlib import file_digest, sha256
import importlib
import json
import os
from pathlib import Path
import shutil
import struct
import sys
import time

BUILD = "27.0.1+2503222"
ENGINE = "8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340"
HOST = "2d5b5f3a49860faa091141e265554e70fd7f41eaced6aab5d263df548fc8500e"
LAB_COMMIT = "91f2eba57fac0b7fbd3dff616056907e3ce461be"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    with Path(path).open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf8"))


def rows(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf8").splitlines() if line.strip()]


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2) + "\n", encoding="utf8")


def event(log, name):
    found = [r for r in log if r.get("event") == name]
    require(len(found) == 1, f"Expected exactly one {name}")
    return found[0]


class NativeLab:
    def __init__(self, runtime, game, artifacts):
        self.runtime, self.game, self.artifacts = (Path(p).resolve() for p in (runtime, game, artifacts))
        for key in list(os.environ):
            if key.startswith("FM27_"):
                del os.environ[key]
        self.root = self.runtime / "engine"
        os.environ.update(FM27_ENGINE_ROOT=str(self.root), FM27_GAME_ROOT=str(self.game),
                          FM27_DESKTOP_DATA=str(self.artifacts / "lab-data"))
        require(digest(self.game / "fm_Data/Plugins/x86_64/game_plugin.dll") == ENGINE, "Engine build changed: revalidate")
        require(digest(self.root / "fm27_native/FM27Simulator.exe") == HOST, "Unvalidated native host")
        require("fm27_tactics_server" not in sys.modules, "Use a fresh process for each Lab runtime")
        sys.path.insert(0, str(self.runtime / "source"))
        self.server = importlib.import_module("fm27_tactics_server")
        status = self.server.ENGINE_COMPATIBILITY
        require(status.get("compatible") is True and status.get("original_build_verified") is True
                and status.get("adapter_version") == BUILD, "Native compatibility gate failed")
        self.fixture = self.root / "fm27_native/fixtures/match.pkm"
        self.identity = dict(build=BUILD, engine_sha256=ENGINE, adapter_host_sha256=HOST,
                             adapter_version=status["profile"], lab_version="v1114.6", lab_commit=LAB_COMMIT,
                             fixture_sha256=digest(self.fixture), resource_fingerprint=status["resource_fingerprint"])

    def baseline(self):
        """Own 4-2-3-1 baseline, both active rosters 23, native side identities retained."""
        s = self.server
        config = deepcopy(s.DEFAULT)
        by_position = {c["position"]: c for c in config["teams"][1]["phases"][0]}
        config["teams"][0]["phases"][0][5:8] = [deepcopy(by_position[p]) for p in ("DMR", "DML", "AMC")]
        for team in config["teams"]:
            team["roster_size"] = 23
        return s.validate_scenario(config)

    def mirror(self, config):
        return self.server.validate_scenario(dict(config, teams=[
            self.server.transplant_team(config["teams"][1], 0),
            self.server.transplant_team(config["teams"][0], 1)]))

    def encode(self, config, path):
        blob = self.server.encode_scenario(config, absolute=True)
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        require(not path.exists() or path.read_bytes() == blob, "Refusing to overwrite a different setup")
        path.write_bytes(blob)
        return sha256(blob).hexdigest()

    def audit_dump(self, path, config):
        actual = read(path)["teams"]
        require(len(actual) == 2, "Missing native team dump")
        for side, (team, wanted) in enumerate(zip(actual, config["teams"], strict=True)):
            count = wanted.get("roster_size", len(wanted["players"]))
            require(team["side"] == side and team["count"] == count, "Native roster size differs")
            require([(p["id"], p["attributes"]) for p in team["players"]] ==
                    [(p["native_id"], p["attributes"]) for p in wanted["players"][:count]], "Native attributes or identity differ")
            require(bytes.fromhex(team["creator_hex"])[0x25] == wanted["mentality"], "Mentality readback differs")
            for phase, cells in enumerate(wanted["phases"]):
                for index, cell in enumerate(cells):
                    slot = self.server.OOP_MAP[side][index] if phase else index
                    raw = bytes.fromhex(team["tactical_slots"][phase][slot])
                    require(struct.unpack_from("<I", raw)[0] == self.server.POSITIONS[cell["position"]]["mask"], "Native phase position differs")
                    require(struct.unpack_from("<Q", raw, 64)[0] == int(self.server.ROLES[cell["role"]]["flags"]) | int(cell["duty"]), "Native role/duty differs")

    def run(self, jobs, directory, workers=1, full=False, bounded_validation=False):
        """No hidden retries; retain every attempt, including integrity failures."""
        from desktop_warm_batch import DesktopWarmRunner, inspect_saved_run
        import desktop_warm_batch
        directory = Path(directory).resolve()
        require(not directory.exists(), "Attempt directory already exists; retain it and choose a new attempt")
        require(type(workers) is int and 1 <= workers <= 4, "Research worker cap is four")
        directory.mkdir(parents=True)
        tasks, by_name = [], {}
        for job in jobs:
            name = job["key"]
            require(name not in by_name and all(c.isalnum() or c in "-_." for c in name), "Unsafe or duplicate job key")
            require(type(job["seed"]) is int and 0 < job["seed"] <= 0xffffffff, "Invalid controlled seed")
            require(Path(job["binary"]).read_bytes() == self.server.encode_scenario(job["config"], absolute=True), "Encoded input changed")
            task = dict(variant=name, seed=job["seed"], scenario=job["config"], config=job["binary"],
                        path=directory / f"{name}.jsonl", dump=directory / f"{name}.input.json",
                        fixture=job.get("fixture", self.fixture), event_details=full,
                        position_names={p["mask"]: p["id"] for p in self.server.POSITIONS.values()})
            tasks.append(task)
            by_name[name] = job, task
        runner = DesktopWarmRunner(self.root, workers=workers, retries=0, timeout=90)
        write(directory / "attempt-manifest.json", dict(identity=self.identity,
              adapter_source_sha256=digest(Path(__file__)), bounded_validation=bounded_validation,
              jobs=[dict(key=j["key"], seed=j["seed"], arm=j["arm"], side=j["side"],
                         setup_sha256=digest(j["binary"])) for j in jobs]))
        results = []
        started = time.perf_counter()
        ledger = directory / "ledger.jsonl"

        def callback(result):
            job, task = by_name[result["variant"]]
            row = dict(self.identity, key=job["key"], seed=job["seed"], arm=job["arm"],
                       tested_side=job["side"], setup_sha256=digest(job["binary"]), status="failed")
            try:
                require(not result.get("failed"), "Native worker failed")
                require(result.get("verified") is True and result["collector_sha256"] == HOST
                        and result["engine_dll_sha256"] == ENGINE, "Native provenance mismatch")
                checked = inspect_saved_run(directory, result)
                require(checked["seed"]["override"] and checked["seed"]["effective_seed"] == job["seed"], "Effective seed differs")
                log = directory / result["log"]
                evidence = rows(log)
                rb = event(evidence, "native_scenario_readback_verified")
                count = struct.unpack_from("<I", Path(job["binary"]).read_bytes(), 8)[0]
                require(rb["after_original_preparation"] and rb["records"] == count, "Input records not read back")
                event(evidence, "native_profile_bindings_verified")
                require(event(evidence, "native_player_tactic_bindings_verified")["players"] == 22, "Player tactics not bound")
                phases = [r for r in evidence if r.get("event") == "native_phase_configuration"]
                require(len(phases) == 4 and {(p["side"], p["phase"]) for p in phases} == {(a,b) for a in (0,1) for b in (0,1)}, "Missing phase receipts")
                self.audit_dump(task["dump"], job["config"])
                statistics = event(evidence, "native_match_statistics")
                require(statistics["source"] == "original_team_statistics" and [t["side"] for t in statistics["teams"]] == [0, 1], "Statistics source differs")
                row.update(status="ok", engine_readback=True, score=checked["result"]["score"],
                           finish_tick=checked["result"]["tick"], team_statistics=[{k:t[k] for k in
                           ("xg","shots","shots_on_target","passes","completed_passes","possession","possession_ticks")} for t in statistics["teams"]],
                           raw_log_sha256=digest(log), input_dump_sha256=digest(task["dump"]),
                           startup_receipt_sha256=result["startup_receipt_sha256"],
                           native_elapsed_seconds=result["native_elapsed_seconds"], worker_job_index=result["worker_job_index"],
                           events_verified=bool(result.get("events",{}).get("collected")))
                require(0 < row["finish_tick"] < 47996, "Invalid natural finish")
                from .stats import metrics
                metrics(row)
            except Exception as error:
                row.update(status="failed", error_type=type(error).__name__)
                write(directory / f"{job['key']}.failure.json", dict(detail=str(error), native_result=result))
                runner.cancel()
            with ledger.open("a", encoding="utf8") as stream:
                stream.write(json.dumps(row, allow_nan=False) + "\n")
                stream.flush()
                os.fsync(stream.fileno())
            results.append(row)
            print(f"{directory.name}: {len(results)}/{len(tasks)} {row['status']}", flush=True)

        original_space_check = desktop_warm_batch.require_space
        def bounded_space_check(path, additional_bytes=0):
            used = sum(p.stat().st_size for p in self.artifacts.rglob("*") if p.is_file())
            require(used + additional_bytes < 512 * 1024**2, "Validation artifact budget exceeded")
            require(shutil.disk_usage(path).free > 2 * 1024**3 + additional_bytes, "Validation disk reserve insufficient")
        if bounded_validation:
            require(len(tasks) <= 16, "Bounded validation batch cap exceeded")
            desktop_warm_batch.require_space = bounded_space_check
        try:
            runner.run(tasks, callback)
        except Exception as error:
            write(directory / "batch-failure.json", dict(error_type=type(error).__name__, detail=str(error),
                  completed_callbacks=len(results), planned=len(tasks)))
            raise
        finally:
            desktop_warm_batch.require_space = original_space_check
            write(directory / "sessions.json", runner.session_diagnostics)
        require(len(results) == len(tasks) and all(r["status"] == "ok" for r in results), "Batch incomplete or input audit failed")
        return results, dict(workers=workers, matches=len(results), wall_seconds=time.perf_counter()-started,
                             session_count=len(runner.session_diagnostics))
