from dataclasses import dataclass, field

from converter.fluka.cards.card import Card
from converter.fluka.helper_parsers.scoring_parser import Scoring


@dataclass
class ScoringsCard:

    data: list[Scoring] = field(default_factory=lambda: [])
    binning_what = "10.0"
    unit_what = "11.0"

    def __str__(self) -> str:
        # each Scoring card consists of two cards;
        # the second one is continuation of data included in first

        # temporary default for no symmetry
        result = ""

        for scoring in self.data:
            first_card = self.handle_first_card(scoring)
            second_card = self.handle_second_card(scoring)

            result += first_card
            result += second_card

        return result

    def handle_first_card(self, scoring: Scoring) -> str:
        x_max = scoring.detector.x_max
        y_max = scoring.detector.y_max
        z_max = scoring.detector.z_max

        first_card = Card(tag="USRBIN")
        first_card.what = [
            self.binning_what,
            self.unit_what,
            x_max,
            y_max,
            z_max
        ]

        return first_card.__str__()

    def handle_second_card(self, scoring: Scoring) -> str:
        # TODO

        second_card = Card(tag="USRBIN")
        return second_card.__str__()
