from dataclasses import dataclass, field
from converter.fluka.cards.card import Card

@dataclass
class MaterialCard(Card):
    """
    Class representing description of single-element material in FLUKA input
    Card consists of codewd which is always "MATERIAL",
    what - a list of 6 parameters (more info https://flukafiles.web.cern.ch/manual/chapters/description_input/description_options/material.html#material),
    sdum which is a name of the material
    """
    codewd: str = "MATERIAL"