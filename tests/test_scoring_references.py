import copy
import json
from pathlib import Path

import pytest

from converter.api import get_parser_from_str, run_parser

TESTS = Path(__file__).parent
PROJECTS = {
    "shieldhit": TESTS / "shieldhit" / "resources" / "project.json",
    "fluka": TESTS / "fluka" / "project.json",
    "geant4": TESTS / "geant4" / "resources" / "project.json",
}


def load_project(simulator: str) -> dict:
    """Return a fresh copy of the test project of the simulator."""
    with open(PROJECTS[simulator], "r") as file_handle:
        return copy.deepcopy(json.load(file_handle))


def convert(simulator: str, project: dict) -> dict:
    """Convert the project with the parser of the simulator."""
    return run_parser(get_parser_from_str(simulator), project)


def first_filtered_quantity(project: dict) -> tuple[dict, dict]:
    """Return the first output with a filtered quantity and that quantity."""
    for output in project["scoringManager"]["outputs"]:
        for quantity in output["quantities"]:
            if quantity.get("filter"):
                return output, quantity
    raise AssertionError("The test project has no filtered quantity")


@pytest.mark.parametrize("simulator", PROJECTS)
def test_project_converts(simulator: str) -> None:
    """Test that the unchanged test projects still convert."""
    assert convert(simulator, load_project(simulator))


@pytest.mark.parametrize("simulator", PROJECTS)
def test_removed_detector(simulator: str) -> None:
    """Test that an output pointing to a removed detector names the output."""
    project = load_project(simulator)
    output = project["scoringManager"]["outputs"][0]
    output["detectorUuid"] = "removed-detector"

    with pytest.raises(
        ValueError,
        match=rf'^Output "{output["name"]}" uses a detector that does not exist \(uuid removed-detector\)\.$',
    ):
        convert(simulator, project)


@pytest.mark.parametrize("simulator", PROJECTS)
def test_removed_filter(simulator: str) -> None:
    """Test that a quantity pointing to a removed filter names the quantity and its output."""
    project = load_project(simulator)
    output, quantity = first_filtered_quantity(project)
    quantity["filter"] = "removed-filter"

    with pytest.raises(
        ValueError,
        match=rf'^Quantity "{quantity["name"]}" in output "{output["name"]}" uses a filter that does not exist '
        r"\(uuid removed-filter\)\.$",
    ):
        convert(simulator, project)


@pytest.mark.parametrize("simulator", PROJECTS)
@pytest.mark.parametrize("filter_uuid", ["", None])
def test_filter_checked_but_not_selected(simulator: str, filter_uuid) -> None:
    """Test that a quantity with Filter checked but no filter selected names the quantity and its output."""
    project = load_project(simulator)
    output, quantity = first_filtered_quantity(project)
    quantity["filter"] = filter_uuid

    with pytest.raises(
        ValueError,
        match=rf'^Quantity "{quantity["name"]}" in output "{output["name"]}" has Filter checked but no filter selected\.$',
    ):
        convert(simulator, project)


@pytest.mark.parametrize("detector_uuid", ["absent", None, ""])
def test_shieldhit_output_without_detector(detector_uuid) -> None:
    """Test that a SHIELD-HIT12A output without a detector names the output."""
    project = load_project("shieldhit")
    output = project["scoringManager"]["outputs"][0]
    if detector_uuid == "absent":
        del output["detectorUuid"]
    else:
        output["detectorUuid"] = detector_uuid

    with pytest.raises(ValueError, match=rf'^Output "{output["name"]}" has no detector selected\.$'):
        convert("shieldhit", project)


def test_shieldhit_zone_output() -> None:
    """Test that a SHIELD-HIT12A zone output explains that zone scoring is not supported."""
    project = load_project("shieldhit")
    output = project["scoringManager"]["outputs"][0]
    output["scoringType"] = "ZONE"
    output["detectorUuid"] = None
    output["zoneUuid"] = project["zoneManager"]["zones"][0]["uuid"]

    with pytest.raises(ValueError, match=rf'^Output "{output["name"]}" scores in a zone'):
        convert("shieldhit", project)


@pytest.mark.parametrize("simulator", ["fluka", "geant4"])
def test_output_without_detector_is_skipped(simulator: str) -> None:
    """Test that FLUKA and Geant4 still skip outputs without a detector, e.g. zone outputs."""
    project = load_project(simulator)
    project["scoringManager"]["outputs"][0]["detectorUuid"] = None

    assert convert(simulator, project)
