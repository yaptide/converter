from dataclasses import dataclass, field
from converter.fluka.cards.card import Card
from converter.fluka.helper_parsers.material_parser import IonisationPotential


@dataclass
class MatpropsCard:
    """
    Class representing description of material properties in FLUKA input.
    Every material assignment is represented by one line:
        codwed - "MAT-PROP"
        what(1) - 0 - ignored
        what(2) - 0 - ignored
        what(3) - average ionisation potential
        what(4) - material name
        what(5) - empty, default what(4)
        what(6) - 0 step length in assigning indices
        sdum - empty
    documentation: https://flukafiles.web.cern.ch/manual/chapters/description_input/description_options/mat-prop.html#mat-prop skipcq: FLK-W505
    """

    data: list[IonisationPotential] = field(default_factory=list)
    codewd: str = "MAT-PROP"

    def __str__(self) -> str:
        """Return card as string."""
        result = ""
        for ionisation_potential in self.data:
            what = [
                0.0,
                0.0,
                ionisation_potential.ionisation_potential,
                ionisation_potential.material_name,
                "",
                0.0,
            ]
            result += str(Card(self.codewd, what)) + "\n"
        return result.strip()
