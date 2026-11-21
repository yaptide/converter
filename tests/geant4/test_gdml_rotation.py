import json
import xml.etree.ElementTree as ET
from pathlib import Path

from converter.api import get_parser_from_str, run_parser

PROJECT_PATH = Path(__file__).parent / "resources" / "project.json"


def gdml_rotations(water_rotation: list[float]) -> list[ET.Element]:
    """Convert the test project with the water cylinder rotated, return all <rotation> elements of the GDML."""
    with open(PROJECT_PATH, "r") as file_handle:
        project = json.load(file_handle)
    water = project["figureManager"]["figures"][0]["children"][0]["children"][0]  # World -> Vacuum -> Water
    water["geometryData"]["rotation"] = water_rotation
    gdml = run_parser(get_parser_from_str("geant4"), project)["geometry.gdml"]
    return list(ET.fromstring(gdml.split("\n", 1)[1]).iter("rotation"))  # skip the XML declaration


def test_unrotated_figure_has_no_rotation():
    assert gdml_rotations([0, 0, 0]) == []


def test_rotation_is_written_with_negated_angles():
    rotations = gdml_rotations([30, 40, 50])
    assert len(rotations) == 1
    assert [float(rotations[0].get(axis)) for axis in "xyz"] == [-30, -40, -50]
