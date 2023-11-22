import pytest
from converter.fluka.helper_parsers.scoring_parser import parse_scorings

@pytest.fixture(scope='module')
def detectors_json(project_fluka_json):
    """zoneManager part of Fluka project.json file"""
    return project_fluka_json['detectorManager']

@pytest.fixture(scope='module')
def scorings_json(project_fluka_json):
    """zoneManager part of Fluka project.json file"""
    return project_fluka_json['scoringManager']

def test_parse_scoring(detectors_json, scorings_json):
    scorings = parse_scorings(detectors_json, scorings_json)