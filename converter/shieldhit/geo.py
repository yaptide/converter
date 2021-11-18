from converter.solid_figures import SolidFigure, BoxFigure, CylinderFigure, SphereFigure
from abc import ABC
from dataclasses import dataclass, field
from math import log10, ceil


def format_float(number: float, n: int) -> float:
    """
    Format float to be up to n characters wide, as precise as possible and as short
    as possible (in descending priority). so for example given 12.333 for n=5 you will
    get 12.33, n=7 will be 12.333
    """
    # If number is zero we just want to get 0.0 (it would mess up the log10 operation below)
    if number == 0:
        return 0.0

    # Sign messes up the log10 we use do determine how long the number is (we fix that with abs).
    # Since there is no sign function in python we use `if else`
    sign = -1 if number < 0 else 1
    result = float(sign*round(abs(number), n-ceil(log10(number))-1))

    # Check if the round function truncated the number, warn the user if it did.
    if result != number:
        print(f'WARN: number was truncated when converting: {number} -> {result}')

    return result


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
          {p7:>10}{p8:>10}""".format(
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
  SPH {number:>4}{p1:>10}{p2:>10}{p3:>10}{p4:>10}""".format(
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
    figures_operators: list[set[int]] = field(default_factory=lambda: [{1}])
    material: str = "1"

    zone_template: str = """
  {id:03d}       {operators}"""

    def __str__(self) -> str:
        return self.zone_template.format(
            id=self.id,
            operators='OR'.join(['  '.join(['{0:+5}'.format(id)
                                 for id in set])
                                 for set in self.figures_operators]),
        )


@dataclass
class GeoMatConfig:
    """Class mapping of the geo.dat config file."""

    figures: list[SolidFigure] = field(default_factory=lambda: [SphereFigure()])
    zones: list[Zone] = field(default_factory=lambda: [Zone()])
    materials: list[int] = field(default_factory=lambda: [276])
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

    material_template: str = """MEDIUM {idx:d}
ICRU {mat:d}
END
"""

    geo_template: str = """
{jdbg1:>5}{jdbg1:>5}          {title}
{figures}
  END
{zones_geometries}
  END
{zones_materials}
"""

    def _get_zone_material_string(self) -> str:
        """Generate material_id, zone_id pairs string (for geo.dat)."""
        zone_ids = "".join(['{0:>5}'.format(zone.id) for zone in self.zones])
        material_ids = "".join(['{0:>5}'.format(zone.material) for zone in self.zones])
        return "\n".join([zone_ids, material_ids])

    def get_geo_string(self) -> str:
        """Generate geo.dat config."""
        return self.geo_template.format(
            jdbg1=self.jdbg1,
            jdbg2=self.jdbg2,
            title=self.title,
            figures="".join([parse_figure(figure, idx) for idx, figure in enumerate(self.figures)])[1:],
            zones_geometries="".join([str(zone) for zone in self.zones])[1:],
            zones_materials=self._get_zone_material_string(),
        )

    def get_mat_string(self) -> str:
        """Generate mat.dat config."""
        material_strings = [self.material_template.format(idx=idx, mat=mat) for idx, mat in enumerate(self.materials)]
        return "\n".join(material_strings)
