import pytest

from converter.fluka.helper_parsers.detector_parser import parse_detector
from converter.fluka.helper_parsers.scoring_parser import parse_scorings

@pytest.fixture(scope='module')
def detectors_json(project_fluka_json):
    """zoneManager part of Fluka project.json file"""
    return project_fluka_json['detectorManager']


def test_parse_scoring(detectors_json):
    scorings = parse_detector(detectors_json, 'c5d0bfa1-525a-4c22-bcc6-3b1d40e1fea3')
