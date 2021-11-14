from converter.solid_figures import SolidFigure, BoxFigure, CylinderFigure, SphereFigure
from abc import ABC
from dataclasses import dataclass
from math import log10, ceil


def format_float(number: float, n: int) -> float:
    """
    Format float to be up to n characters wide, as precise as possible and as short
    as possible (in descending priority). so for example given 12.333 for n=5 you will
    get 12.33, n=7 will be 12.333
    """
    if(number == 0):
        return 0.0

    return float(round(number, n-ceil(log10(number))-1))


def parse_figure(figure: SolidFigure, number: int) -> str:
    """Parse a SolidFigure into a str representation of SH12A input file."""
    if type(figure) is BoxFigure:
        return _parse_box(figure, number)
    elif type(figure) is CylinderFigure:
        return _parse_cylinder(figure, number)
    elif type(figure) is SphereFigure:
        return _parse_sphere(figure, number)
    else:
        raise ValueError("Unexpected solid figure type: {}".format(type(figure)))


def _parse_box(box: BoxFigure, number: int) -> str:
    """Parse a BoxFigure into a str representation of SH12A input file."""
    return """
  BOX {number:>4}{p1:>10}{p2:>10}{p3:>10}{p4:>10}{p5:>10}{p6:>10}
          {p7:>10}{p8:>10}{p9:>10}{p10:>10}{p11:>10}{p12:>10}""".format(
        number=number,
        p1=format_float(box.position[0]-box.x_edge_length/2, 10),
        p2=format_float(box.position[1]-box.y_edge_length/2, 10),
        p3=format_float(box.position[2]-box.z_edge_length/2, 10),
        p4=format_float(box.x_edge_length, 10),
        p5=format_float(0, 10),
        p6=format_float(0, 10),
        p7=format_float(0, 10),
        p8=format_float(box.y_edge_length, 10),
        p9=format_float(0, 10),
        p10=format_float(0, 10),
        p11=format_float(0, 10),
        p12=format_float(box.z_edge_length, 10),
    )


def _parse_cylinder(cylinder: CylinderFigure, number: int) -> str:
    """Parse a CylinderFigure into a str representation of SH12A input file."""
    return """
  TRC {number:>4}{p1:>10}{p2:>10}{p3:>10}{p4:>10}{p5:>10}{p6:>10}
          {p7:>10}{p8:>10}{padding:>40}""".format(
        number=number,
        p1=format_float(cylinder.position[0], 10),
        p2=format_float(cylinder.position[1]-cylinder.height/2, 10),
        p3=format_float(cylinder.position[2], 10),
        p4=format_float(0, 10),
        p5=format_float(cylinder.height, 10),
        p6=format_float(0, 10),
        p7=format_float(cylinder.radius_bottom, 10),
        p8=format_float(cylinder.radius_top, 10),
        padding='',
    )


def _parse_sphere(sphere: SphereFigure, number: int) -> str:
    """Parse a SphereFigure into a str representation of SH12A input file."""
    return """
  SPH {number:>4}{p1:>10}{p2:>10}{p3:>10}{p4:>10}{padding:>20}""".format(
        number=number,
        p1=format_float(sphere.position[0], 10),
        p2=format_float(sphere.position[1], 10),
        p3=format_float(sphere.position[2], 10),
        p4=format_float(sphere.radius, 10),
        padding='',
    )


@dataclass
class Zone():
    """Dataclass mapping for SH12A zones."""

    id: int = 1
    figures_operators: list[tuple[int, str]] = [(1, '')]
    material: str = "1"

    zone_template: str = """
  {id:03d}       {operators:>63}
"""

    def __str__(self) -> str:
        return self.zone_template.format(
            id=self.id,
            operators=''.join(['{0:+5}{1:>2}'.format(id, operation)
                               for id, operation in self.figures_operators]),
        )


@dataclass
class GeoConfig:
    """Class mapping of the geo.dat config file."""

    figures: list[SolidFigure] = [SphereFigure()]
    zones: list[Zone] = [Zone()]
    jdbg1: int = 0
    jdbg2: int = 0
    title: str = "Unnamed geometry"

#     geo_template: str = """
# *---><---><--------><------------------------------------------------>
# {jdbg1:>5}{jdbg1:>5}          {title:>60}
# *---><---><--------><--------><--------><--------><--------><-------->{figures}
# END
# {zones}
# END
# {materials}
# """

    geo_template: str = """
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
        return self.geo_template
