import pytest

from converter.fluka.helper_parsers.detector_parser import parse_detector


@pytest.fixture(scope='module')
def detectors_json(project_fluka_json):
    return project_fluka_json['detectorManager']


def test_parse_scoring(detectors_json):
    detector_dict = next(
        (detector for detector in detectors_json['detectors'] if detector['uuid'] == 'c5d0bfa1-525a-4c22-bcc6-3b1d40e1fea3'),
        None
    )
    assert detector_dict

    detector = parse_detector(detector_dict)

    assert detector

    assert detector.name == 'Detector'
    assert detector.x_min == -0.05
    assert detector.x_max == 0.05
    assert detector.x_bins == 1
    assert detector.y_min == -5
    assert detector.y_max == 5
    assert detector.y_bins == 100
    assert detector.z_min == -6
    assert detector.z_max == 6
    assert detector.z_bins == 120
