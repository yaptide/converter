from dataclasses import dataclass, field
from converter.common import format_float

from converter.fluka.helper_parsers.figure_parser import FlukaBox, FlukaCylinder, FlukaFigure, FlukaSphere


@dataclass
class FiguresCard:
    """Class representing description of figures in Fluka input"""

    data: list[FlukaFigure] = field(default_factory=lambda: [])

    def __str__(self) -> str:
        """Return the card as a string."""
        result = ""
        for index, figure in enumerate(self.data):
            if index == 0:
                line = ""
            else:
                line = "\n"
            line += f"{figure.figure_type} {figure.name}"
            if type(figure) is FlukaBox:
                line += (f" {format_float(figure.coordinates[0], n=16):+#}"
                         f" {format_float(figure.coordinates[1], n=16):+#}"
                         f" {format_float(figure.coordinates[2], n=16):+#}"
                         f" {format_float(figure.x_vector[0], n=16):+#}"
                         f" {format_float(figure.x_vector[1], n=16):+#}"
                         f" {format_float(figure.x_vector[2], n=16):+#}\n"
                         f"{format_float(figure.y_vector[0], n=16):+#}"
                         f" {format_float(figure.y_vector[1], n=16):+#}"
                         f" {format_float(figure.y_vector[2], n=16):+#}"
                         f" {format_float(figure.z_vector[0], n=16):+#}"
                         f" {format_float(figure.z_vector[1], n=16):+#}"
                         f" {format_float(figure.z_vector[2], n=16):+#}")
            elif type(figure) is FlukaCylinder:
                line += (f" {format_float(figure.coordinates[0], n=16):+#}"
                         f" {format_float(figure.coordinates[1], n=16):+#}"
                         f" {format_float(figure.coordinates[2], n=16):+#}"
                         f" {format_float(figure.height_vector[0], n=16):+#}"
                         f" {format_float(figure.height_vector[1], n=16):+#}\n"
                         f"{format_float(figure.height_vector[2], n=16):+#}"
                         f" {format_float(figure.radius, n=16):+#}")
            elif type(figure) is FlukaSphere:
                line += (f" {format_float(figure.coordinates[0], n=16):+#}"
                         f" {format_float(figure.coordinates[1], n=16):+#}"
                         f" {format_float(figure.coordinates[2], n=16):+#}"
                         f" {format_float(figure.radius, n=16):+#}")
            else:
                raise ValueError(f"Unexpected figure type: {figure}")

            result += line

        return result
