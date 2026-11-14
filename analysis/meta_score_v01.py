#!/usr/bin/env python3
"""Exploratory FM27 within-position meta index v0.1. No game/engine access."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Mapping

MODEL_FILE = Path(__file__).resolve().parents[1] / "research" / "meta_score_v01_weights.json"
ALIASES = {
    "IV": "CB", "DC": "CB", "CB": "CB",
    "LV": "FB", "RV": "FB", "DL": "FB", "DR": "FB",
    "WBL": "FB", "WBR": "FB", "WB": "FB", "FB": "FB",
    "DM": "DM", "DMC": "DM", "6": "DM",
    "CM": "CM", "MC": "CM", "8": "CM",
    "AM": "AM", "AMC": "AM", "AML": "AM", "AMR": "AM",
    "LM": "AM", "RM": "AM", "10": "AM",
    "ST": "ST", "STC": "ST", "9": "ST",
    "GK": "GK", "TW": "GK",
}


def load_model(path: Path = MODEL_FILE) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data["schema_version"] != 1 or data["model_id"] != "FM27_META_SCORE_V0_1":
        raise ValueError("Unsupported model or schema.")
    for position, config in data["positions"].items():
        if sum(config["weights_pct"].values()) != 100:
            raise ValueError(f"{position}: weight sum must equal 100.")
    return data


def _score(weights: Mapping[str, float], attrs: Mapping[str, float]) -> float:
    return sum(weight * (attrs[key] - 1.0) for key, weight in weights.items()) / (
        19.0 * sum(weights.values()) / 100.0
    )


def evaluate(position: str, attributes: Mapping[str, float], model: dict | None = None) -> dict:
    """Return a weighted scouting index and heuristic (NOT statistical) context band.

    Attribute names are the English snake_case keys from the model JSON. All
    required visible 1..20 attributes must be supplied. Unknown extra fields
    are ignored, never interpreted as verified evidence.
    """
    if model is None:
        model = load_model()
    key = ALIASES.get(str(position).upper())
    if key is None or key not in model["positions"]:
        raise ValueError(f"Unknown position {position!r}; expected CB, FB, DM, CM, AM, ST or GK.")
    weights = model["positions"][key]["weights_pct"]
    clean = {}
    for attr in weights:
        if attr not in attributes:
            raise ValueError(f"Missing attribute {attr!r} for {key}.")
        x = attributes[attr]
        if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or not (1 <= x <= 20):
            raise ValueError(f"Invalid attribute {attr!r}: {x!r}. Expected a finite 1..20 value.")
        clean[attr] = float(x)

    score = _score(weights, clean)
    source_scores = {}
    for name, source_weights in model["positions"][key].get("source_weights_fraction", {}).items():
        # Convert fractions to percentage weights for the same _score helper.
        source_scores[name] = _score({a: b * 100 for a, b in source_weights.items()}, clean)

    if len(source_scores) == 2:
        low = min(source_scores.values()) - 3
        high = max(source_scores.values()) + 3
    else:
        low, high = score - 5, score + 5
    return {
        "model": model["model_id"],
        "position": key,
        "score": round(score, 2),
        "source_scenario_scores": {k: round(v, 2) for k, v in source_scores.items()},
        "heuristic_gray_band": [round(max(0.0, low), 2), round(min(100.0, high), 2)],
        "gray_band_is_statistical_confidence_interval": False,
        "is_calibrated_match_performance_prediction": False,
    }


def compare(position: str, first: Mapping[str, float], second: Mapping[str, float],
            model: dict | None = None) -> dict:
    if model is None:
        model = load_model()
    a = evaluate(position, first, model)
    b = evaluate(position, second, model)
    if a["heuristic_gray_band"][0] > b["heuristic_gray_band"][1]:
        verdict = "FIRST_FAVORED_WITHIN_MODELED_CONTEXTS"
    elif b["heuristic_gray_band"][0] > a["heuristic_gray_band"][1]:
        verdict = "SECOND_FAVORED_WITHIN_MODELED_CONTEXTS"
    else:
        verdict = "GRAY_OVERLAP"
    return {"first": a, "second": b, "score_difference": round(a["score"] - b["score"], 2),
            "verdict": verdict, "verdict_is_calibrated_probability": False}


def main() -> None:
    parser = argparse.ArgumentParser(description="Exploratory FM27 meta index (NOT a win probability).")
    parser.add_argument("--position", required=True, help="CB, FB, DM, CM, AM, ST, GK or alias.")
    parser.add_argument("--attributes-file", required=True, type=Path,
                        help="JSON file with snake_case English attribute names and 1..20 values.")
    parser.add_argument("--compare-file", type=Path, default=None,
                        help="Optional second JSON profile for same-position comparison.")
    args = parser.parse_args()
    first = json.loads(args.attributes_file.read_text(encoding="utf-8"))
    if not isinstance(first, dict):
        parser.error("Expected a JSON object with attributes.")
    if args.compare_file:
        second = json.loads(args.compare_file.read_text(encoding="utf-8"))
        result = compare(args.position, first, second)
    else:
        result = evaluate(args.position, first)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
