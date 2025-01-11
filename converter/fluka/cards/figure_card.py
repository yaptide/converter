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
            if type(figure) is FlukaBox:
                x_min = format_float(figure.x_min, n=16)
                x_max = format_float(figure.x_max, n=16)
                y_min = format_float(figure.y_min, n=16)
                y_max = format_float(figure.y_max, n=16)
                z_min = format_float(figure.z_min, n=16)
                z_max = format_float(figure.z_max, n=16)
                x_length = format_float(figure.x_max - figure.x_min, n=16)
                y_length = format_float(figure.y_max - figure.y_min, n=16)
                z_length = format_float(figure.z_max - figure.z_min, n=16)
                line += (f"* box {figure.name}\n"
                         f"* X range {x_min:+#}, {x_max:+#}\n"
                         f"* Y range {y_min:+#}, {y_max:+#}\n"
                         f"* Z range {z_min:+#}, {z_max:+#}\n"
                         f"* X, Y, Z side lengths:"
                         f" {x_length:+#}, {y_length:+#}, {z_length:+#}\n"
                         f"{figure.figure_type} {figure.name}"
                         f" {x_min:+#}"
                         f" {x_max:+#}"
                         f" {y_min:+#}"
                         f" {y_max:+#}"
                         f" {z_min:+#}"
                         f" {z_max:+#}")
            elif type(figure) is FlukaCylinder:
                x = format_float(figure.coordinates[0], n=16)
                y = format_float(figure.coordinates[1], n=16)
                z = format_float(figure.coordinates[2], n=16)
                vector_x = format_float(figure.height_vector[0], n=16)
                vector_y = format_float(figure.height_vector[1], n=16)
                vector_z = format_float(figure.height_vector[2], n=16)
                top_x = format_float(figure.coordinates[0] + figure.height_vector[0], n=16)
                top_y = format_float(figure.coordinates[1] + figure.height_vector[1], n=16)
                top_z = format_float(figure.coordinates[2] + figure.height_vector[2], n=16)
                radius = format_float(figure.radius, n=16)
                height = format_float(figure.height, n=16)
                line += (f"* cylinder {figure.name}\n"
                         f"* bottom center ({x:+#}, {y:+#}, {z:+#}),"
                         f" top center ({top_x:+#}, {top_y:+#}, {top_z:+#})\n"
                         f"* spanning vector ({vector_x:+#}, {vector_y:+#}, {vector_z:+#})\n"
                         f"* radius {radius:+#}, height {height:+#} cm\n"
                         f"* rotation angles: {figure.rotation[0]}*, "
                         f"{figure.rotation[1]}*, {figure.rotation[2]}*\n"
                         f"{figure.figure_type} {figure.name}"
                         f" {x:+#}"
                         f" {y:+#}"
                         f" {z:+#}"
                         f" {vector_x:+#}"
                         f" {vector_y:+#}\n"
                         f"{vector_z:+#}"
                         f" {radius:+#}")
            elif type(figure) is FlukaSphere:
                x = format_float(figure.coordinates[0], n=16)
                y = format_float(figure.coordinates[1], n=16)
                z = format_float(figure.coordinates[2], n=16)
                radius = format_float(figure.radius, n=16)
                line += (f"* sphere {figure.name}\n"
                         f"* center ({x:+#}, {y:+#}, {z:+#}),"
                         f" radius {radius:+#}\n"
                         f"{figure.figure_type} {figure.name}"
                         f" {x:+#}"
                         f" {y:+#}"
                         f" {z:+#}"
                         f" {radius:+#}")
            else:
                raise ValueError(f"Unexpected figure type: {figure}")

            result += line

        return result
