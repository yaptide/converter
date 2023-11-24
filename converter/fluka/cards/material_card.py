from dataclasses import dataclass, field
from converter.fluka.helper_parsers.material_parser import FlukaMaterial
from converter.fluka.cards.card import Card


@dataclass
class MaterialsCard:
    """
    Class representing description of materials in Fluka input.
    Every material is represented by one line:
        codwed - "MATERIAL"
        what(1) - atomic number
        what(2) - empty, computed according to what(1)
        what(3) - density in g/cm^3
        what(4) - empty, we are using name-based input
        what(5) - 0 - ignored
        what(6) - 0 - natural composition of the what(1) element
        sdum - Name of the material
    documentation: https://flukafiles.web.cern.ch/manual/chapters/description_input/description_options/material.html#material
    """

    data: list[FlukaMaterial] = field(default_factory=list)
    codewd: str = "MATERIAL"

    def __str__(self) -> str:
        """Return card as string."""
        result = ""
        for material in self.data:
            what = [material.Z, "", material.density, "", 0, 0]
            sdum = material.fluka_name
            result += str(Card(self.codewd, what, sdum)) + "\n"
        return result
