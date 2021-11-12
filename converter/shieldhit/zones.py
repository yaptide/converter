from converter.solid_figures import SolidFigure, BoxFigure, CylinderFigure, SphereFigure
from abc import ABC
from dataclasses import dataclass


def SolidFigureParser():
    """
    Wrapper class for solid figures parser. Used to parse any solid figure into a SH12A 
    input file format.
    """

    def parse(figure: SolidFigure) -> str:
        """Parse a SolidFigure into a str representation of SH12A input file."""
        pass

    def _parse_box(box: BoxFigure) -> str:
        """Parse a BoxFigure into a str representation of SH12A input file."""
        pass

    def _parse_cylinder(cylinder: CylinderFigure) -> str:
        """Parse a CylinderFigure into a str representation of SH12A input file."""
        pass

    def _parse_sphere(sphere: SphereFigure) -> str:
        """Parse a SphereFigure into a str representation of SH12A input file."""
        pass


@dataclass
def Zone():

    figures: list[SolidFigure]
    operators: list[str]
    material: str

    template: str = """
*---><---><--------><------------------------------------------------>
    0    0           protons, H2O 30 cm cylinder, r=10, 1 zone
*---><---><--------><--------><--------><--------><--------><-------->
  RCC    1       0.0       0.0       0.0       0.0       0.0      30.0
                10.0
  RCC    2       0.0       0.0      -5.0       0.0       0.0      35.0
                15.0
  RCC    3       0.0       0.0     -10.0       0.0       0.0      40.0
                20.0
  END
  001          +1
  002          +2     -1
  003          +3     -2
  END
* material codes: 1 - liquid water (ICRU material no 276), 1000 - vacuum, 0 - black body
    1    2    3
    1 1000    0
"""

    def __str__(self) -> str:
        return self.template
