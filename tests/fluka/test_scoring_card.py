import pytest

from converter.fluka.cards.scoring_card import ScoringsCard
from converter.fluka.helper_parsers.scoring_parser import parse_scorings


@pytest.fixture(scope='module')
def scorings_json(project_fluka_json) -> dict:
    return project_fluka_json['scoringManager']


@pytest.fixture(scope='module')
def detectors_json(project_fluka_json) -> dict:
    return project_fluka_json['detectorManager']


@pytest.fixture(scope='module')
def scorings_json_2(project2_fluka_json: dict) -> dict:
    return project2_fluka_json['scoringManager']


@pytest.fixture(scope='module')
def detectors_json_2(project2_fluka_json: dict) -> dict:
    return project2_fluka_json['detectorManager']


@pytest.fixture(scope='module')
def scorings_json_3(project3_fluka_json: dict) -> dict:
    return project3_fluka_json['scoringManager']


@pytest.fixture(scope='module')
def detectors_json_3(project3_fluka_json: dict) -> dict:
    return project3_fluka_json['detectorManager']


@pytest.fixture(scope='module')
def scorings_json_4(project4_fluka_json: dict) -> dict:
    return project4_fluka_json['scoringManager']


@pytest.fixture(scope='module')
def detectors_json_4(project4_fluka_json: dict) -> dict:
    return project4_fluka_json['detectorManager']


def expected_card() -> str:
    """Returns expected Fluka scoring card sets"""
    lines = """
USRBIN          10.0  ALL-PART     -21.0      0.05       5.0       6.0Fluence_21
USRBIN         -0.05      -5.0      -6.0       1.0     100.0     120.0&
AUXSCORE      USRBIN -100100.0                 1.0       1.0       1.0
"""

    return lines.strip()


@pytest.fixture(scope='module')
def expected_scores() -> str:
    """Returns expected Fluka scoring card sets"""
    lines = """
USRBIN          10.0  ALL-PART     -21.0      0.05       5.0       6.0Flue_TzG3O
USRBIN         -0.05      -5.0      -6.0       1.0     100.0     120.0&
AUXSCORE      USRBIN -100100.0                 1.0       1.0       1.0
"""

    return lines.strip()


@pytest.fixture(scope='module')
def expected_scores_2() -> str:
    """Returns expected Fluka scoring card sets"""
    lines = """
USRBIN          10.0  ALL-PART     -21.0      0.05       5.0       6.0Flue_TzG3O
USRBIN         -0.05      -5.0      -6.0       1.0     100.0     120.0&
AUXSCORE      USRBIN -100100.0                 1.0       1.0       1.0
USRBIN          10.0      DOSE     -22.0      12.5      25.0      37.5MyDo_dX4W2
USRBIN           7.5      15.0      22.5      10.0     100.0     150.0&
AUXSCORE      USRBIN   NEUTRON                 2.0       2.0       1.0
"""

    return lines.strip()


@pytest.fixture(scope='module')
def expected_scores_cylinder() -> str:
    """Returns expected Fluka scoring card sets"""
    lines = """
USRBIN          11.0      DOSE     -21.0       3.0       0.0      21.0Dose_Tt536
USRBIN           0.0       0.0       3.0       1.0       1.0     100.0&
"""

    return lines.strip()


@pytest.fixture(scope='module')
def expected_scores_4() -> str:
    """Returns expected Fluka scoring card sets"""
    lines = """
USRBIN          10.0      DOSE     -21.0       2.5       2.5      21.0D_To_-l6m6
USRBIN          -2.5      -2.5       3.0       1.0       1.0     100.0&
USRBIN          10.0      DOSE     -21.0       2.5       2.5      21.0D_Pr_EWZdl
USRBIN          -2.5      -2.5       3.0       1.0       1.0     100.0&
AUXSCORE      USRBIN    PROTON                 2.0       2.0       1.0
USRBIN          10.0      DOSE     -21.0       2.5       2.5      21.0D_He_q3AVx
USRBIN          -2.5      -2.5       3.0       1.0       1.0     100.0&
AUXSCORE      USRBIN  3-HELIUM                 3.0       3.0       1.0
USRBIN          10.0      DOSE     -21.0       2.5       2.5      21.0D_C__8Y1Bp
USRBIN          -2.5      -2.5       3.0       1.0       1.0     100.0&
AUXSCORE      USRBIN-1200600.0                 4.0       4.0       1.0
USRBIN          10.0      DOSE     -21.0       2.5       2.5      21.0D_He_oeZGk
USRBIN          -2.5      -2.5       3.0       1.0       1.0     100.0&
AUXSCORE      USRBIN -400200.0                 5.0       5.0       1.0
USRBIN          10.0      DOSE     -21.0       2.5       2.5      21.0D_B__HBQJv
USRBIN          -2.5      -2.5       3.0       1.0       1.0     100.0&
AUXSCORE      USRBIN -900400.0                 6.0       6.0       1.0
USRBIN          11.0  ALL-PART     -22.0       2.5       0.0      21.0F_To_SNVdq
USRBIN           0.0       0.0       3.0       1.0       1.0     100.0&
USRBIN          11.0    PROTON     -22.0       2.5       0.0      21.0F_Pr_7CgH1
USRBIN           0.0       0.0       3.0       1.0       1.0     100.0&
USRBIN          11.0  3-HELIUM     -22.0       2.5       0.0      21.0F_He_KCn1N
USRBIN           0.0       0.0       3.0       1.0       1.0     100.0&
USRBIN          11.0  ALL-PART     -22.0       2.5       0.0      21.0F_C__w6biy
USRBIN           0.0       0.0       3.0       1.0       1.0     100.0&
AUXSCORE      USRBIN-1200600.0                10.0      10.0       1.0
USRBIN          11.0  ALL-PART     -22.0       2.5       0.0      21.0F_He_WQwN-
USRBIN           0.0       0.0       3.0       1.0       1.0     100.0&
AUXSCORE      USRBIN -400200.0                11.0      11.0       1.0
USRBIN          11.0  ALL-PART     -22.0       2.5       0.0      21.0F_B__WYZoZ
USRBIN           0.0       0.0       3.0       1.0       1.0     100.0&
AUXSCORE      USRBIN -900400.0                12.0      12.0       1.0
"""

    return lines.strip()


def test_scoring_card(detectors_json: dict, scorings_json: dict, expected_scores: str) -> None:
    scorings = parse_scorings(detectors_json, scorings_json)
    scorings_card = ScoringsCard(scorings)

    assert str(scorings_card) == expected_scores


def test_scoring_card_multiple_scorings(detectors_json_2: dict, scorings_json_2: dict, expected_scores_2: str) -> None:
    scorings = parse_scorings(detectors_json_2, scorings_json_2)
    scorings_card = ScoringsCard(scorings)

    assert str(scorings_card) == expected_scores_2


def test_scoring_cylinder_detector(detectors_json_3: dict, scorings_json_3: dict,
                                   expected_scores_cylinder: str) -> None:
    scorings = parse_scorings(detectors_json_3, scorings_json_3)
    scorings_card = ScoringsCard(scorings)

    assert str(scorings_card) == expected_scores_cylinder


def test_scoring_dose_and_fluence_with_two_detectors(detectors_json_4: dict, scorings_json_4: dict,
                                                     expected_scores_4: str) -> None:
    scorings = parse_scorings(detectors_json_4, scorings_json_4)
    scorings_card = ScoringsCard(scorings)

    assert str(scorings_card) == expected_scores_4
