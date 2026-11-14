"""Read-only ingestion of career checkpoints; never substitutes single-match simulation."""
from collections import defaultdict
from pathlib import Path

from .native import read, require

CONTROL_FIELDS = ("start_save_sha256", "build", "coaches_sha256", "roster_sha256", "calendar_sha256", "opponents_sha256")


def validate_checkpoints(checkpoints, arms, weeks):
    require(checkpoints and len(arms)>=2 and len(set(arms))==len(arms), "Career design missing")
    indexed={}
    for row in checkpoints:
        key=(row["replicate"],row["arm"],row["week"])
        require(key not in indexed and row["arm"] in arms and row["week"] in weeks, "Duplicate/unknown checkpoint")
        require(row.get("calendar_readback_verified") is True and row.get("individual_exposure_verified") is True,
                "Calendar and individual exposure readback required")
        require(all(row.get(k) for k in CONTROL_FIELDS) and row.get("checkpoint_sha256") and
                row.get("intervention_readback_sha256") and row.get("outcomes"), "Missing career provenance/outcomes")
        indexed[key]=row
    replicates={r["replicate"] for r in checkpoints}
    expected={(rep,arm,week) for rep in replicates for arm in arms for week in weeks}
    require(indexed.keys()==expected, "Incomplete career branches/checkpoints")
    for rep in replicates:
        group=[indexed[rep,arm,week] for arm in arms for week in weeks]
        require(all(all(r[k]==group[0][k] for k in CONTROL_FIELDS) for r in group), "Career control drift")
    return dict(replicates=len(replicates), branches=len(replicates)*len(arms), checkpoints=len(checkpoints),
                independent_unit="career_branch; players are nested repeated observations",
                automatic_game_execution_validated=False)


def import_checkpoints(paths, arms, weeks):
    data=[read(Path(path)) for path in paths]
    return validate_checkpoints(data,arms,weeks)
