from dataclasses import dataclass, field

from converter.fluka.cards.card import Card
from converter.fluka.helper_parsers.scoring_parser import Scoring


def handle_first_card(scoring: Scoring) -> str:
    """Creates first Scoring card"""
    # temporary assumption
    binning_what = "10.0"
    # DOSE according to:
    # https://flukafiles.web.cern.ch/manual/chapters/particle_and_material_codes/particles_codes.html
    particle_of_scoring = "DOSE"
    # Fixed for now
    output_unit = '-21'

    first_card = Card(codewd="USRBIN")
    first_card.what = [
        binning_what,
        particle_of_scoring,
        output_unit,
        scoring.detector.x_max,
        scoring.detector.y_max,
        scoring.detector.z_max
    ]
    first_card.sdum = 'changeme'

    return first_card.__str__()


def handle_second_card(scoring: Scoring) -> str:
    """Creates second Scoring card"""
    second_card = Card(codewd="USRBIN")
    second_card.what = [
        scoring.detector.x_min,
        scoring.detector.y_min,
        scoring.detector.z_min,
        scoring.detector.x_bins,
        scoring.detector.y_bins,
        scoring.detector.z_bins,
    ]
    second_card.sdum = '&'

    return second_card.__str__()


@dataclass
class ScoringsCard:
    """Class representing ScoringCard"""

    data: list[Scoring] = field(default_factory=list)

    def __str__(self) -> str:
        # each Scoring card consists of two cards;
        # the second one is continuation of data included in first

        # temporary default for no symmetry
        result = ""

        for scoring in self.data:
            first_card = handle_first_card(scoring)
            second_card = handle_second_card(scoring)
            result += f"{first_card}\n{second_card}\n"

        return result
