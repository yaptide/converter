import pytest
from converter.fluka.helper_parsers.scoring_parser import parse_scorings

@pytest.fixture(scope='module')
def detectors_json(project_fluka_json):
    return project_fluka_json['detectorManager']

@pytest.fixture(scope='module')
def scorings_json(project_fluka_json):
    return project_fluka_json['scoringManager']

def test_parse_scoring(detectors_json, scorings_json):
    scorings = parse_scorings(detectors_json, scorings_json)

    assert scorings[0].name == 'yz slab'
    assert scorings[0].detectorUuid == 'c5d0bfa1-525a-4c22-bcc6-3b1d40e1fea3'
    assert scorings[0].quantity == 'DOSE'
