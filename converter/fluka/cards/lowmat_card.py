from dataclasses import dataclass, field
from converter.fluka.helper_parsers.material_parser import FlukaLowMat
from converter.fluka.cards.card import Card


@dataclass
class LowMatsCard:
    """
    Class representing description of low-energy neutron cross sections in Fluka input.
    Every material is represented by one line:
        codwed - "LOW-MAT"
        what(1) - Name of the Fluka material
        what(3) - what(6) not used
        sdum - Name of the low-energy neutron material
        documentation: https://flukafiles.web.cern.ch/manual/chapters/description_input/description_options/low-mat.html#low-mat # skipcq: FLK-W505
    """

    data: list[FlukaLowMat] = field(default_factory=list)
    codewd: str = "LOW-MAT"

    def __str__(self) -> str:
        """Return card as string."""
        result = ""
        for lowmat in self.data:
            what = [lowmat.material_name]
            sdum = lowmat.low_energy_neutron_material
            result += str(Card(self.codewd, what, sdum)) + "\n"
        return result.strip()
