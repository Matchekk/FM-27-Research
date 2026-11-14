"""Render released SHARPNESS-P0 effects only; never runs or imports a simulator."""
from argparse import ArgumentParser
from hashlib import sha256
from io import BytesIO
import json
from math import isclose, isfinite, sqrt
from pathlib import Path

EXPERIMENT = "MECH-002-SHARPNESS-P0"
CONTEXTS = ("high_press", "deep_block")
SECONDARY = {"SHARPNESS:points", "SHARPNESS:gf", "SHARPNESS:ga",
             "SHARPNESS:xgf", "SHARPNESS:xga", "PRESS:xgd", "SHARPNESSxPRESS:xgd"}
INTERVENTION = "Verified original twenty-record raw10000-minus7000 start package, stamina60 fixed"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def number(value):
    require(type(value) in (int, float) and isfinite(value), "Expected finite number")
    return float(value)


def interval(value):
    require(type(value) is list and len(value) == 2, "Expected two interval bounds")
    lo, hi = map(number, value)
    require(lo <= hi, "Reversed interval bounds")
    return lo, hi


def context_interval(mean, sd):
    """Descriptive marginal context t interval: 32 paired seed-side means, df31."""
    from scipy.stats import t
    mean, sd = number(mean), number(sd)
    require(sd >= 0, "Negative context SD")
    half = float(t.ppf(.975, 31)) * sd / sqrt(32)
    return mean - half, mean + half


def validate_estimate(value):
    mean, se = number(value["mean"]), number(value["se"])
    require(se >= 0 and value["alpha"] == .05, "Invalid SE or interval level")
    require(type(value["n_seed_blocks"]) is int and value["n_seed_blocks"] == 64 and
            type(value["n_scenarios"]) is int and value["n_scenarios"] == 2,
            "Expected 64 complete paired seed blocks across two contexts")
    require(value["weighting"] == "equal_scenarios_then_equal_seeds; sides averaged within seed",
            "Wrong context/side weighting")
    ci = interval(value["ci"])
    boot = interval(value["bootstrap_ci"])
    require(isclose(sum(ci) / 2, mean, abs_tol=1e-10), "Welch interval is not centered")
    require(set(value["context"]) == set(CONTEXTS), "Unexpected contexts")
    contexts = []
    for key in CONTEXTS:
        cell = value["context"][key]
        cm, sd = number(cell["mean"]), number(cell["sd"])
        require(sd >= 0, "Negative context SD")
        contexts.append(dict(key=key, mean=cm, ci=context_interval(cm, sd), sd=sd))
    require(isclose(mean, sum(c["mean"] for c in contexts) / 2, abs_tol=1e-10),
            "Overall mean disagrees with equal context weights")
    expected_se = sqrt(sum(c["sd"] ** 2 for c in contexts) / 128)
    require(isclose(se, expected_se, rel_tol=1e-9, abs_tol=1e-12),
            "SE disagrees with 32 complete blocks per context")
    p = number(value["p"])
    require(0 <= p <= 1, "Invalid p value")
    return dict(mean=mean, ci=ci, bootstrap_ci=boot, context=contexts)


def validate_inputs(effects, summary, manifest):
    """Fail closed on incomplete/failed studies; shape checks are not raw-data review."""
    require(summary.get("phase") == "main" and
            all(summary.get(k) is True for k in
                ("passed", "complete", "budget_reconciled", "scientific_analysis_allowed")),
            "Main release is absent, incomplete, failed or unreconciled")
    require(type(summary.get("full_matches")) is int and summary["full_matches"] == 512 and
            type(summary.get("negative_rejections")) is int and summary["negative_rejections"] == 0,
            "Expected 512 valid main matches without a main rejection")
    require(effects.get("experiment_id") == EXPERIMENT and
            type(effects.get("n_matches")) is int and effects["n_matches"] == 512 and
            type(effects.get("independent_seed_blocks")) is int and effects["independent_seed_blocks"] == 64 and
            effects.get("primary_contrast") == "SHARPNESS", "Wrong study, contrast or sample size")
    require(effects.get("intervention") == INTERVENTION, "Raw start-package scope differs")
    require(all(effects.get(k) is False for k in
                ("ui_scale_calibrated", "consumer_semantics_validated", "mediation_identified",
                 "career_transfer_confirmed", "winner_selected")) and
            effects.get("exploratory_context_and_side_only") is True,
            "Unsupported interpretation or context inference")
    require(effects.get("bootstrap", {}).get("resamples") == 20000 and
            effects.get("practical_reference") == .3 and effects.get("desired_full_ci_width") == .5,
            "Preregistered uncertainty/reference settings differ")
    require(set(effects["secondary"]) == SECONDARY, "Expected exact Holm7 secondary family")
    for result in effects["secondary"].values():
        p = number(result["p_holm"])
        require(0 <= p <= 1 and type(result["reject_holm"]) is bool and
                result["reject_holm"] == (p <= .05), "Malformed Holm7 result")
    config = manifest["config"]
    require(config["experiment_id"] == EXPERIMENT and config["status"] == "registered",
            "Wrong or unregistered manifest")
    design, science, native = config["design"], config["science"], config["native_spec"]
    require(type(design["n_blocks"]) is int and design["n_blocks"] == 32 and
            design["sides"] == [0, 1] and [s["id"] for s in design["scenarios"]] == list(CONTEXTS) and
            all(s["split"] == "discovery" for s in design["scenarios"]), "Wrong context/block/side design")
    require(science["context_weights"] == [.5, .5] and science["side_weights"] == [.5, .5] and
            science["family_size"] == 7 and science["multiple_testing"] == "holm" and
            science["contrast_coefficients"]["SHARPNESS"] == [-.5, .5, -.5, .5],
            "Wrong registered weighting, contrast or family")
    require(native["raw_levels"] == [7000, 10000] and native["profile_fields"] == [16, 17] and
            native["stamina_raw"] == 60 and native["encoded_stamina_records"] == 46 and
            native["ui_scale_calibrated"] is False, "Wrong raw package or fixed Stamina")
    seeds = manifest["seeds"]
    require(len(seeds) == len(set(seeds)) == 64 and all(type(s) is int for s in seeds),
            "Expected 64 distinct registered seed blocks")
    identity = config["identity"]
    require(type(identity["build"]) is str and bool(identity["build"]), "Missing registered engine build")
    for key in ("engine_sha256", "fixture_sha256"):
        text = identity[key]
        require(type(text) is str and len(text) == 64 and all(c in "0123456789abcdef" for c in text),
                "Missing registered identity hash")
    primary = validate_estimate(effects["primary"])
    points = validate_estimate(effects["secondary"]["SHARPNESS:points"])
    return dict(primary=primary, points=points, build=identity["build"],
                points_holm_p=effects["secondary"]["SHARPNESS:points"]["p_holm"])


def read_json(path):
    require(path.is_file() and path.stat().st_size <= 8 * 1024 ** 2, "Missing/oversized public JSON")
    def unique(pairs):
        out = {}
        for key, value in pairs:
            require(key not in out, "Duplicate JSON field")
            out[key] = value
        return out
    raw = path.read_bytes()
    return json.loads(raw, object_pairs_hook=unique,
                      parse_constant=lambda token: require(False, "Nonfinite JSON constant")), sha256(raw).hexdigest()


def render(model, hashes, output):
    """Write one self-contained SVG after release validation; never overwrite an artifact."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    require(output.suffix.lower() == ".svg", "Standalone SVG output required")
    require(not output.exists(), "Refusing to overwrite an existing artifact")
    style = {"font.family": "DejaVu Sans", "font.size": 10, "svg.fonttype": "path",
             "svg.hashsalt": "fm27-sharpness002-figure-v1", "axes.titleweight": "bold",
             "figure.facecolor": "white", "axes.facecolor": "white"}
    with plt.rc_context(style):
        fig, axes = plt.subplots(1, 2, figsize=(12.2, 6.4))
        fig.subplots_adjust(left=.19, right=.97, top=.72, bottom=.29, wspace=.42)
        titles = ("xGD · primär", "Tatsächliche Punkte · sekundär")
        labels = ("Gesamt · Welch95", "Gesamt · Bootstrap95",
                  "Hohes Pressing · explorativ", "Tiefer Block · explorativ")
        for ax, title, name, unit in zip(axes, titles, ("primary", "points"), ("xGD", "Punkte")):
            value = model[name]
            rows = [(3.2, value["mean"], value["ci"], "#205c8c", "o"),
                    (2.5, value["mean"], value["bootstrap_ci"], "#b86822", "s")]
            rows.extend((y, c["mean"], c["ci"], "#66737f", "D")
                        for y, c in zip((1.15, .35), value["context"]))
            for y, mean, (lo, hi), color, marker in rows:
                ax.plot([lo, hi], [y, y], color=color, linewidth=2.3, solid_capstyle="round")
                ax.scatter([mean], [y], color=color, marker=marker, s=38, zorder=3)
            bounds = [v for _, mean, ci, _, _ in rows for v in (*ci, mean)] + [0.]
            low, high = min(bounds), max(bounds)
            margin = max((high - low) * .14, .05)
            ax.set_xlim(low - margin, high + margin)
            ax.axvline(0, color="#8a9299", linewidth=1, linestyle=(0, (3, 3)))
            ax.axhline(1.9, color="#dce1e5", linewidth=.8)
            ax.set_yticks([3.2, 2.5, 1.15, .35], labels if name == "primary" else [""] * 4)
            ax.set_ylim(-.1, 3.65)
            ax.tick_params(axis="y", length=0, pad=10)
            ax.grid(axis="x", color="#e9edf0", linewidth=.7)
            ax.set_axisbelow(True)
            ax.set_xlabel(f"Differenz {unit} pro Match", labelpad=9)
            ax.set_title(title, loc="left", pad=15, fontsize=12)
            for spine in ("top", "right", "left"):
                ax.spines[spine].set_visible(False)
            ax.spines["bottom"].set_color("#bdc6cc")
        fig.text(.055, .93, "Originales Rohwert-Startpaket: 10000 minus 7000", fontsize=17, weight="bold")
        fig.text(.055, .875, f"{EXPERIMENT}  |  Build {model['build']}  |  512 Matches / 64 Seedblöcke", fontsize=10.5)
        fig.text(.055, .83, "D00 · gebündeltes synthetisches Fixture · zwei Discoverygegner · beide Seiten", fontsize=10, color="#45525d")
        fig.text(.055, .18, "Gesamt: gleiche Kontextgewichte; Seitenmittel je Seed. Bootstrap: 20.000 stratifizierte Seedblockziehungen.", fontsize=9)
        fig.text(.055, .14, "Kontexte: deskriptive marginale 95-%-t-Intervalle (je 32 Blöcke, df 31), keine bestätigten Moderatoreffekte.", fontsize=9)
        fig.text(.055, .10, f"Alle Intervalle marginal, nicht simultan. Punkte gehören zu Holm7 (adjustiertes p={model['points_holm_p']:.4g}).", fontsize=9)
        fig.text(.055, .06, "Keine kalibrierte UI-Prozentskala, Consumer-/Mediationsaussage oder bestätigte Karriereübertragung.", fontsize=9)
        fig.text(.055, .025, "SHA256: " + " · ".join(f"{name} {value[:12]}" for name, value in hashes.items()), fontsize=7, color="#64717b")
        buffer = BytesIO()
        try:
            fig.savefig(buffer, format="svg", metadata={"Date": None, "Creator": "FM27 Research / render_sharpness002.py"})
        finally:
            plt.close(fig)
    payload = "\n".join(line.rstrip() for line in buffer.getvalue().decode("utf-8").splitlines()) + "\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as stream:
        stream.write(payload.encode("utf-8"))
    return sha256(payload.encode("utf-8")).hexdigest()


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--effects", required=True, type=Path)
    parser.add_argument("--summary", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    require(args.validate_only or args.output is not None, "Specify --output or --validate-only")
    effects, eh = read_json(args.effects)
    summary, sh = read_json(args.summary)
    manifest, mh = read_json(args.manifest)
    model = validate_inputs(effects, summary, manifest)
    if args.validate_only:
        print(json.dumps(dict(valid=True, rendered=False, experiment_id=EXPERIMENT, input_sha256=dict(effects=eh, summary=sh, manifest=mh))))
        return
    require(args.output.resolve() not in {p.resolve() for p in (args.effects, args.summary, args.manifest)},
            "Output aliases an input")
    digest = render(model, dict(effects=eh, summary=sh, manifest=mh), args.output)
    print(json.dumps(dict(rendered=True, svg_sha256=digest, experiment_id=EXPERIMENT)))


if __name__ == "__main__":
    main()
