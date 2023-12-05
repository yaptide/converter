from dataclasses import dataclass, field

from converter.fluka.cards.card import Card
from converter.fluka.helper_parsers.scoring_parser import Scoring


@dataclass
class ScoringsCard:
    """Class representing set of scoring cards in Fluka"""

    data: list[Scoring] = field(default_factory=list)

    def __str__(self) -> str:
        """Returns string representation of all scoring cards"""
        result = ''

        default_output_unit = 21
        for scoring in self.data:
            scoring.output_unit = default_output_unit
            result += str(scoring)
            default_output_unit += 1
        return result
