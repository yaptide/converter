from dataclasses import dataclass

from converter.fluka.cards.card import Card


@dataclass
class ScoringsCard(Card):

    def __str__(self) -> str:

        """Return the card as a string."""
        title = "* scoring DOSE on mesh"
        return title

    def __post_init__(self):

        # temporary assumption, that quantity is DOSE, independently from user's choice
        self.what[0] = "DOSE"