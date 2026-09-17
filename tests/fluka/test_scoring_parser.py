import pytest
from converter.fluka.helper_parsers.scoring_parser import parse_scorings


@pytest.fixture(scope="module")
def detectors_json(project_fluka_json):
    """Return detector manager JSON from the Fluka project fixture."""
    return project_fluka_json["detectorManager"]


@pytest.fixture(scope="module")
def scorings_json(project_fluka_json):
    """Return scoring manager JSON from the Fluka project fixture."""
    return project_fluka_json["scoringManager"]


def test_parse_scoring(detectors_json, scorings_json):
    """Test parsing scorings and verify quantity and detector properties."""
    scorings = parse_scorings(detectors_json, scorings_json)

    assert scorings[0].quantities[0].name == "Fluence"
    assert scorings[0].detector.name == "Detector"
    assert scorings[0].quantities[0].keyword == "Fluence"
