from dataclasses import dataclass, field

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
            line += "{} {}".format(figure.figure_type, figure.name)
            if type(figure) is FlukaBox:
                line += (f" {figure.coordinates[0]:+#.16g} {figure.coordinates[1]:+#.16g}"
                         f" {figure.coordinates[2]:+#.16g} {figure.x_vector[0]:+#.16g}"
                         f" {figure.x_vector[1]:+#.16g} {figure.x_vector[2]:+#.16g}\n"
                         f"{figure.y_vector[0]:+#.16g} {figure.y_vector[1]:+#.16g}"
                         f" {figure.y_vector[2]:+#.16g} {figure.z_vector[0]:+#.16g}"
                         f" {figure.z_vector[1]:+#.16g} {figure.z_vector[2]:+#.16g}")
            elif type(figure) is FlukaCylinder:
                line += (f" {figure.coordinates[0]:+#.16g} {figure.coordinates[1]:+#.16g}"
                         f" {figure.coordinates[2]:+#.16g} {figure.height_vector[0]:+#.16g}"
                         f" {figure.height_vector[1]:+#.16g}\n{figure.height_vector[2]:+#.16g}"
                         f" {figure.radius:+#.16g}")
            elif type(figure) is FlukaSphere:
                line +=(f" {figure.coordinates[0]:+#.16g} {figure.coordinates[1]:+#.16g}"
                        f" {figure.coordinates[2]:+#.16g} {figure.radius:+#.16g}")
            else:
                raise ValueError(f"Unexpected figure type: {figure}")

            result += line

        return result
