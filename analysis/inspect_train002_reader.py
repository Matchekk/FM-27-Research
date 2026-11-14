"""Static installed-reader inventory. Reads Python text, never imports fmsave/host."""
import ast
import hashlib
import importlib.metadata
import json
from pathlib import Path


def inspect_installed_reader():
    distribution = importlib.metadata.distribution("fmsave")
    package = Path(distribution.locate_file("fmsave"))
    files = {}
    for relative in ("_save.py", "models/training.py", "models/players.py", "models/injuries.py"):
        raw = (package / relative).read_bytes()
        tree = ast.parse(raw.decode("utf8"))
        classes = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name in ("TrainingDay", "TrainingWeek", "TeamTraining", "InjuryRecord"):
                classes[node.name] = [n.target.id for n in node.body if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)]
        files[relative] = {"sha256": hashlib.sha256(raw).hexdigest(), "selected_model_fields": classes}
    return {"origin": "installed_package_static_source_inspection", "package": "fmsave",
            "version": distribution.version, "files": files,
            "save_files_opened": 0, "native_matches_started": 0, "calendar_advances": 0,
            "empirical_current_build_reader_validation": False,
            "career_released": False}


if __name__ == "__main__":
    print(json.dumps(inspect_installed_reader(), indent=2, allow_nan=False))
