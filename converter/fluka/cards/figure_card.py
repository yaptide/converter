from dataclasses import dataclass, field

from converter.fluka.helper_parsers.figure_parser import FlukaBox, FlukaCylinder, FlukaFigure, FlukaSphere


@dataclass
class FiguresCard:
    """Class representing description of figures in Fluka input"""
    data: list[FlukaFigure] = field(default_factory=lambda: [])

    def __str__(self) -> str: #line max 132 chars, add plus sign before positive numbers
        """Return the card as a string."""
        result = ""
        for index, figure in enumerate(self.data):
            if index == 0:
                line = ""
            else:
                line = "\n"
            line += "{} {}".format(figure.figure_type, figure.name)
            if type(figure) is FlukaBox:
                line += """ {:+.16g} {:+.16g} {:+.16g} {:+.16g} {:+.16g} {:+.16g}\n
                {:+.16g} {:+.16g} {:+.16g} {:+.16g} {:+.16g} {:+.16g}""".format(
                    figure.coordinates[0],
                    figure.coordinates[1],
                    figure.coordinates[2],
                    figure.x_vector[0],
                    figure.x_vector[1],
                    figure.x_vector[2],
                    figure.y_vector[0],
                    figure.y_vector[1],
                    figure.y_vector[2],
                    figure.z_vector[0],
                    figure.z_vector[1],
                    figure.z_vector[2],
                )
            elif type(figure) is FlukaCylinder:
                line += " {:+.16g} {:+.16g} {:+.16g} {:+.16g} {:+.16g}\n{:+.16g} {:+.16g}".format(
                    figure.coordinates[0],
                    figure.coordinates[1],
                    figure.coordinates[2],
                    figure.height_vector[0],
                    figure.height_vector[1],
                    figure.height_vector[2],
                    figure.radius
                )
            elif type(figure) is FlukaSphere:
                line += " {:+.16g} {:+.16g} {:+.16g} {:+.16g}".format(
                    figure.coordinates[0],
                    figure.coordinates[1],
                    figure.coordinates[2],
                    figure.radius
                )
            else:
                raise ValueError(f"Unexpected figure type: {figure}")

            result+=line

        return result