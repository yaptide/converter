from dataclasses import dataclass
from converter.fluka.cards.card import Card


@dataclass
class MaterialCard(Card):
    """
    Class representing description of single-element material in FLUKA input.
    Card consists of:
    - codewd (str): 'MATERIAL'
    - what (list[str]): list of parameters (see FLUKA manual for details)
    - sdum (str): name of the material
    """

    codewd: str = "MATERIAL"
