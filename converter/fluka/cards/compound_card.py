from dataclasses import dataclass, field
from converter.fluka.cards.card import Card


@dataclass
class CompoundCard(Card):
    """
    Class representing description of compound material in FLUKA input.
    Card consists of:
    - codewd (str): 'COMPOUND'
    - what (list[str]): list of parameters (see FLUKA manual for details)
    - sdum (str): name of the compound
    """

    codewd: str = "COMPOUND"
    composition: list[tuple[float, Card]] = field(default_factory=lambda: [])

    def __str__(self) -> str:
        """Return the card as a string."""
        result = ""
        for i in range(0, len(self.composition), 3):
            items = []
            for content, material in self.composition[i : i + 3]:
                items.append(content)
                items.append(
                    material.sdum if material.sdum else str(material.fluka_number)
                )
            self.what = items
            result += self._format_line() + "\n"
        return result

    def add_component(self, content: float, material: Card):
        """Add component to the compound."""
        if len(self.composition) >= 80:
            raise IndexError("Compound can have at most 80 components.")
        self.composition.append((content, material))
