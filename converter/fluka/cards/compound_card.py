from dataclasses import dataclass, field
from converter.fluka.cards.card import Card
from converter.fluka.helper_parsers.material_parser import FlukaCompound


@dataclass
class CompoundsCard:
    """
    Class representing description of compound material in FLUKA input.
    Every compound assignment is represented by one or more lines if
    there are more than 3 components:
        codewd - "COMPOUND"
        what(1) - mass fraction of first material in the compound
        what(2) - name of first material
        what(3) - mass fraction of second material in the compound
        what(4) - name of second material
        what(5) - mass fraction of third material in the compound
        what(6) - name of third material
        sdum - name of the compound
    If there are more than 3 materials in the compound, another lines are added with same sdum
    documentation: https://flukafiles.web.cern.ch/manual/chapters/description_input/description_options/compound.html
    """

    data: list[FlukaCompound] = field(default_factory=list)
    codewd: str = "COMPOUND"

    def __str__(self) -> str:
        """Return the card as a string."""
        result = ""
        for compound in self.data:
            sdum = compound.fluka_name
            for i in range(0, len(compound.composition), 3):
                what = []
                for content, material in compound.composition[i : i + 3]:
                    what.append(content)
                    what.append(material)
                result += Card(self.codewd, what, sdum) + "\n"
        return result
