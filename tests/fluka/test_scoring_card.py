import pytest

from converter.fluka.cards.scoring_card import ScoringsCard
from converter.fluka.helper_parsers.scoring_parser import parse_scorings
from tests.fluka.conftest import project2_fluka_json


@pytest.fixture(scope='module')
def scorings_json(project_fluka_json) -> dict:
    return project_fluka_json['scoringManager']


@pytest.fixture(scope='module')
def detectors_json(project_fluka_json) -> dict:
    return project_fluka_json['detectorManager']


@pytest.fixture(scope='module')
def scorings_json_2(project2_fluka_json) -> dict:
    return project2_fluka_json['scoringManager']


@pytest.fixture(scope='module')
def detectors_json_2(project2_fluka_json) -> dict:
    return project2_fluka_json['detectorManager']


@pytest.fixture(scope="module")
def expected_card() -> str:
    """Returns expected Fluka scoring card sets"""
    line_one = "USRBIN          10.0      DOSE     -21.0      0.05       5.0       6.0changeme"
    line_two = "USRBIN         -0.05      -5.0      -6.0       1.0     100.0     120.0&"

    return f"{line_one}\n{line_two}\n"


@pytest.fixture(scope="module")
def expected_card_2() -> str:
    """Returns expected Fluka scoring card sets"""
    line_one   = "USRBIN          10.0      DOSE     -21.0      0.05       5.0       6.0changeme"
    line_two   = "USRBIN         -0.05      -5.0      -6.0       1.0     100.0     120.0&"
    line_three = "USRBIN          10.0      DOSE     -21.0      12.5      25.0      37.5changeme"
    line_four  = "USRBIN           7.5      15.0      22.5      10.0     100.0     150.0&"
    return f"{line_one}\n{line_two}\n{line_three}\n{line_four}\n"


def test_scoring_card(detectors_json: dict, scorings_json: dict, expected_card: str) -> None:
    scorings = parse_scorings(detectors_json, scorings_json)
    scorings_card = ScoringsCard(scorings)

    assert scorings_card.__str__() == expected_card


def test_scoring_card_multiple_scorings(detectors_json_2: dict, scorings_json_2: dict, expected_card_2: str) -> None:
    scorings = parse_scorings(detectors_json_2, scorings_json_2)
    scorings_card = ScoringsCard(scorings)

    assert scorings_card.__str__() == expected_card_2
