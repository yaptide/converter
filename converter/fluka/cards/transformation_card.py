from dataclasses import dataclass, field
from converter.common import format_float
from converter.fluka.cards.card import Card
from converter.fluka.helper_parsers.figure_parser import FlukaBox, FlukaFigure

# FLUKA reads names given in SDUM from a 10 characters wide column
MAX_NAME_LENGTH = 10


@dataclass
class TransformationsCard:
    """
    Class representing roto-translations of rotated boxes in Fluka input. They have to be
    outside of the geometry description. Every rotated box is represented by three lines
    with the same name, combined by Fluka into one transformation:
        codewd - "ROT-DEFI"
        what(1) - 101, 201, 301: rotation about the X, Y and Z axis
        what(2) - polar angle, always 0
        what(3) - rotation angle
        what(4) - what(6) - translation, applied before the rotation (first line only)
        sdum - name of the transformation
    Used with a minus in $Start_transform (inverse transformation), it rotates the box like the
    editor does (three.js Euler 'XYZ') and moves it to its position.
        documentation: https://flukafiles.web.cern.ch/manual/chapters/description_input/description_options/rot-defi.html # skipcq: FLK-W505
    """

    data: list[FlukaFigure] = field(default_factory=list)
    codewd: str = "ROT-DEFI"

    def __str__(self) -> str:
        """Return card as string."""
        result = ""
        for figure in self.data:
            if type(figure) is not FlukaBox or not figure.is_rotated:
                continue
            name = figure.transformation_name
            if len(name) > MAX_NAME_LENGTH:
                raise ValueError(f"Transformation name {name} is longer than {MAX_NAME_LENGTH} characters")
            angle_x, angle_y, angle_z = (str(format_float(float(angle), 10)) for angle in figure.rotation)
            offsets = [str(format_float(-float(coordinate), 10)) for coordinate in figure.position]
            result += f"* rotation and position of box {figure.name}\n"
            result += str(Card(self.codewd, ["101", "0.0", angle_x, *offsets], name)) + "\n"
            result += str(Card(self.codewd, ["201", "0.0", angle_y], name)) + "\n"
            result += str(Card(self.codewd, ["301", "0.0", angle_z], name)) + "\n"
        return result.strip()
