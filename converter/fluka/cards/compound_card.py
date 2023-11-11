from dataclasses import dataclass, field
from converter.fluka.cards.card import Card
from converter.fluka.cards.material_card import MaterialCard
from typing import List, Tuple

@dataclass
class CompoundCard(Card):
    """
    Class representing description of compound material in FLUKA input
    Card consists of codewd which is always "COMPOUND",
    composition - a list of tuples of (material content of compound*, name of the material),
    sdum which is a name of the compound

    (More info about 'material content of compound' - WHAT(1)
    https://flukafiles.web.cern.ch/manual/chapters/description_input/description_options/compound.html)
    """
    codewd: str = "COMPOUND"
    composition: List[Tuple[float, MaterialCard]] = field(default_factory=lambda: [])

    def __str__(self) -> str:
        """Return the card as a string."""
        result = ""
        for i in range(0, len(self.composition), 3):
            items = []
            for content, material in self.composition[i:i+3]:
                items.append(content)
                items.append(material.sdum)
            items = [item for sublist in self.composition[i:i+3] for item in sublist]
            result += self._format_line(self.codewd, items, self.sdum) + "\n"
        return result
        