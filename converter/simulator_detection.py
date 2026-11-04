import re
from typing import Optional

REQUIRED_INPUT_FILES = {
    "shieldhit": ["beam.dat", "geo.dat", "mat.dat", "detect.dat"],
    "fluka": ["fl_sim.inp"],
    "geant4": ["geometry.gdml", "run.mac"],
}

COPY_SUFFIX_AFTER_EXTENSION = re.compile(r"(.+\.(?:dat|inp|gdml|mac|json))[0-9]+")
COPY_SUFFIX_BEFORE_EXTENSION = re.compile(r"(.+?)(?: ?\([0-9]+\)|-[0-9]+| [0-9]+)(\.[A-Za-z0-9]+)")


def name_without_copy_suffix(name: str) -> Optional[str]:
    """
    Return the original file name if `name` looks like a copy made by the browser
    when the same file is downloaded twice (e.g. `fl_sim (1).inp`, `fl_sim-2.inp`), otherwise None.
    Used only to suggest renaming the file; a copy is never treated as the required file.
    """
    after_extension = COPY_SUFFIX_AFTER_EXTENSION.fullmatch(name)
    if after_extension:
        return after_extension.group(1)

    before_extension = COPY_SUFFIX_BEFORE_EXTENSION.fullmatch(name)
    if before_extension:
        return before_extension.group(1) + before_extension.group(2)

    return None


def required_by(name: str) -> Optional[str]:
    """Return the simulator that requires a file with this exact name, or None."""
    return next((simulator for simulator, names in REQUIRED_INPUT_FILES.items() if name in names), None)


def _inspect_file(name: str) -> dict:
    """Return the simulator that requires the file and the issues found in its name."""
    original_name = name_without_copy_suffix(name)
    issues = []
    if original_name:
        issues.append(
            {
                "severity": "warning",
                "code": "copy_suffix",
                "message": f"Looks like a downloaded copy of {original_name}",
                "suggested_name": original_name,
            }
        )
    return {"simulator": required_by(name), "issues": issues}


def _inspect_simulator(simulator: str, files: dict) -> dict:
    """Return whether the simulator can run with these files and which required files are missing."""
    missing = [name for name in REQUIRED_INPUT_FILES[simulator] if name not in files]
    if missing:
        return {"possible": False, "reason": f"Missing {', '.join(missing)}", "missing": missing}
    return {"possible": True, "missing": []}


def detect_simulators(files: dict) -> dict:
    """Check which simulators can run with the given files (file name -> content); content is not checked."""
    return {
        "files": {name: _inspect_file(name) for name in files},
        "simulators": {simulator: _inspect_simulator(simulator, files) for simulator in REQUIRED_INPUT_FILES},
    }


def get_empty_template(simulator: str) -> dict:
    """Return the required files of the simulator, each with empty content."""
    if simulator not in REQUIRED_INPUT_FILES:
        raise ValueError(f"Simulator must be one of: {', '.join(REQUIRED_INPUT_FILES)}.")
    return {name: "" for name in REQUIRED_INPUT_FILES[simulator]}
