from dataclasses import dataclass, field
from converter.fluka.cards.card import Card
from converter.fluka.helper_parsers.material_parser import MaterialAssignment


@dataclass
class AssignmatsCard:
    """
    Class representing description of material assignment in FLUKA input.
    Every material assignment is represented by one line:
        codwed - "ASSIGNMA"
        what(1) - material name
        what(2) - region name
        sdum - empty, it's not used
    documentation: https://flukafiles.web.cern.ch/manual/chapters/description_input/description_options/assignma.html#assignmat
    """

    data: list[MaterialAssignment] = field(default_factory=list)
    codewd = "ASSIGNMA"

    def __str__(self) -> str:
        """Return card as string."""
        result = ""
        for material_assignment in self.data:
            what = [material_assignment.material_name, material_assignment.region_name]
            result += str(Card(self.codewd, what)) + "\n"
        return result
