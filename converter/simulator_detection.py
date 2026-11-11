import re
from typing import Optional

REQUIRED_INPUT_FILES = {
    "shieldhit": ["beam.dat", "geo.dat", "mat.dat", "detect.dat"],
    "fluka": ["fl_sim.inp"],
    "geant4": ["geometry.gdml", "run.mac"],
}


# Number after the extension.
#   Matches: fl_sim.inp2, run.mac12
#   Does not match: notes.txt2 (not an input file), beam.dat.1
COPY_SUFFIX_AFTER_EXTENSION = re.compile(
    r"""
    (.+\.(?:dat|inp|gdml|mac|json))  # original name
    [0-9]+                           # number
    """,
    re.VERBOSE,
)

# Number before the extension.
#   Matches: fl_sim (1).inp, fl_sim(1).inp, fl_sim-2.inp, fl_sim 2.inp
#   Does not match: sim_2.inp, my-beam.dat, fl_sim (a).inp, fl_sim (1)
COPY_SUFFIX_BEFORE_EXTENSION = re.compile(
    r"""
    (.+?)                                   # name
    (?:\ ?\([0-9]+\)|-[0-9]+|\ [0-9]+)      # " (1)", "(1)", "-1" or " 1"
    (\.[A-Za-z0-9]+)                        # extension
    """,
    re.VERBOSE,
)


def name_without_copy_suffix(name: str) -> Optional[str]:
    """
    Return the original file name if `name` looks like a copy made by the browser
    when the same file is downloaded twice, otherwise None.
    Uses regexes written above to detect the copy suffixes added to the file name.
    Used only to suggest renaming the file; a copy is never treated as the required file.
    """
    after_extension = COPY_SUFFIX_AFTER_EXTENSION.fullmatch(name)
    if after_extension:
        return after_extension.group(1)

    before_extension = COPY_SUFFIX_BEFORE_EXTENSION.fullmatch(name)
    if before_extension:
        return before_extension.group(1) + before_extension.group(2)

    return None


# e.g. "BEAM.DAT" -> "beam.dat", used to find required files written in other letter case
REQUIRED_NAMES_BY_LOWERCASE = {name.lower(): name for names in REQUIRED_INPUT_FILES.values() for name in names}

# Browser copy of any file.
#   Matches: sobp (1).dat, notes(2).txt
#   Does not match: sobp-2.dat, layer 3.dat
BROWSER_COPY_NAME = re.compile(r".+ ?\([0-9]+\)\.[A-Za-z0-9]+")

# e.g. fl_sim.inp.txt saved from Notepad
TEXT_EXTENSION = ".txt"


def required_by(name: str) -> Optional[str]:
    """Return the simulator that requires a file with this exact name, or None."""
    return next((simulator for simulator, names in REQUIRED_INPUT_FILES.items() if name in names), None)


def required_name_ignoring_case(name: str) -> Optional[str]:
    """Return the required file name equal to `name` when letter case is ignored, or None."""
    return REQUIRED_NAMES_BY_LOWERCASE.get(name.lower())


def _rename_warning(code: str, message: str, suggested_name: str) -> dict:
    """Return a warning that suggests renaming a file to `suggested_name`."""
    return {"severity": "warning", "code": code, "message": message, "suggested_name": suggested_name}


def _downloaded_copy_suggestion(name: str) -> Optional[dict]:
    """
    Suggest the original name for a downloaded copy of a required file (`fl_sim (1).inp`, `beam-2.dat`)
    or for a browser copy of any other file (`sobp (1).dat`), otherwise return None.
    """
    original_name = name_without_copy_suffix(name)
    if not original_name:
        return None

    required_name = required_name_ignoring_case(original_name)
    if required_name:
        return _rename_warning("copy_suffix", f"Looks like a downloaded copy of {required_name}", required_name)

    if BROWSER_COPY_NAME.fullmatch(name):
        return _rename_warning("copy_suffix", f"Looks like a downloaded copy of {original_name}", original_name)

    return None


def _text_extension_suggestion(name: str) -> Optional[dict]:
    """Suggest the required name for a required file saved with an extra .txt extension (`fl_sim.inp.txt`)."""
    if not name.lower().endswith(TEXT_EXTENSION):
        return None

    required_name = required_name_ignoring_case(name[: -len(TEXT_EXTENSION)])
    if not required_name:
        return None

    return _rename_warning(
        "extra_extension", f"Looks like {required_name} saved with an extra .txt extension", required_name
    )


def _letter_case_suggestion(name: str) -> Optional[dict]:
    """Suggest the required name for a required file written in other letter case (`BEAM.DAT`)."""
    required_name = required_name_ignoring_case(name)
    if not required_name:
        return None

    return _rename_warning("wrong_case", f"File names are case-sensitive, did you mean {required_name}?", required_name)


def _rename_suggestion(name: str) -> Optional[dict]:
    """Return a warning suggesting a new name for a file that looks like a misnamed required file, or None."""
    if required_by(name):
        return None

    return _downloaded_copy_suggestion(name) or _text_extension_suggestion(name) or _letter_case_suggestion(name)


def _inspect_file(name: str) -> dict:
    """Return the simulator that requires the file and the issues found in its name."""
    suggestion = _rename_suggestion(name)
    return {"simulator": required_by(name), "issues": [suggestion] if suggestion else []}


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
