from converter.solid_figures import SolidFigure, BoxFigure, CylinderFigure, SphereFigure
from abc import ABC
from dataclasses import dataclass, field
from math import log10, ceil, isclose
from scipy.spatial.transform import Rotation as R


def format_float(number: float, n: int) -> float:
    """
    Format float to be up to n characters wide, as precise as possible and as short
    as possible (in descending priority). so for example given 12.333 for n=5 you will
    get 12.33, n=7 will be 12.333
    """
    result = number
    # If number is zero we just want to get 0.0 (it would mess up the log10 operation below)
    if isclose(result, 0.):
        return 0.

    length = n

    # Adjust lenght for decimal separator ('.')
    length -= 1

    # Sign messes up the log10 we use do determine how long the number is. We use
    # abs() to fix that, but we need to remember the sign and update `n` accordingly
    sign = 1

    if result < 0:
        result = abs(result)
        sign = -1
        # Adjust lenght for the sign
        length -= 1

    whole_length = ceil(log10(result))

    # Check if it will be possible to fit the number
    if whole_length > length-1:
        raise ValueError(f"Number is to big to be formatted. Minimum length: {whole_length-sign+1},\
requested length: {n}")

    # Adjust n for the whole numbers, log returns reasonable outputs for values greater
    # than 1, for other values it returns nonpositive numbers, but we would like 1
    # to be returned. We solve that by taking the greater value between the returned and
    # and 1.
    length -= max(whole_length, 1)

    result = float(sign*round(result, length))

    # Check if the round function truncated the number, warn the user if it did.
    if not isclose(result, number):
        print(f'WARN: number was truncated when converting: {number} -> {result}')

    # Formatting negative numbers smaller than the desired precission could result in -0.0 or 0.0 randomly.
    # To avoid this we catch -0.0 and return 0.0.
    if isclose(result, 0.):
        return 0.

    return result


def parse_figure(figure: SolidFigure, number: int) -> str:
    """Parse a SolidFigure into a str representation of SH12A input file."""
    if type(figure) is BoxFigure:
        return _parse_box(figure, number)
    if type(figure) is CylinderFigure:
        return _parse_cylinder(figure, number)
    if type(figure) is SphereFigure:
        return _parse_sphere(figure, number)

    raise ValueError("Unexpected solid figure type: {}".format(figure))


def _parse_box(box: BoxFigure, number: int) -> str:
    """Parse a BoxFigure into a str representation of SH12A input file."""
    rotation = R.from_euler('xyz', box.rotation, degrees=True)
    x_vect = rotation.apply([box.x_edge_length, 0, 0])
    y_vect = rotation.apply([0, box.y_edge_length, 0])
    z_vect = rotation.apply([0, 0, box.z_edge_length])
    diagonal_vect = x_vect+y_vect+z_vect
    start_position = (
        box.position[0] - diagonal_vect[0]/2,
        box.position[1] - diagonal_vect[1]/2,
        box.position[2] - diagonal_vect[2]/2,
    )

    return """
  BOX {number:>4}{p1:>10}{p2:>10}{p3:>10}{p4:>10}{p5:>10}{p6:>10}
          {p7:>10}{p8:>10}{p9:>10}{p10:>10}{p11:>10}{p12:>10}""".format(
        number=number,
        p1=format_float(start_position[0], 10),
        p2=format_float(start_position[1], 10),
        p3=format_float(start_position[2], 10),
        p4=format_float(x_vect[0], 10),
        p5=format_float(x_vect[1], 10),
        p6=format_float(x_vect[2], 10),
        p7=format_float(y_vect[0], 10),
        p8=format_float(y_vect[1], 10),
        p9=format_float(y_vect[2], 10),
        p10=format_float(z_vect[0], 10),
        p11=format_float(z_vect[1], 10),
        p12=format_float(z_vect[2], 10),
    )


def _parse_cylinder(cylinder: CylinderFigure, number: int) -> str:
    """Parse a CylinderFigure into a str representation of SH12A input file."""
    rotation = R.from_euler('xyz', cylinder.rotation, degrees=True)
    height_vect = rotation.apply([0, cylinder.height, 0])
    lower_base_position = (
        cylinder.position[0] - height_vect[0]/2,
        cylinder.position[1] - height_vect[1]/2,
        cylinder.position[2] - height_vect[2]/2,
    )
    return """
  RCC {number:>4}{p1:>10}{p2:>10}{p3:>10}{p4:>10}{p5:>10}{p6:>10}
          {p7:>10}""".format(
        number=number,
        p1=format_float(lower_base_position[0], 10),
        p2=format_float(lower_base_position[1], 10),
        p3=format_float(lower_base_position[2], 10),
        p4=format_float(height_vect[0], 10),
        p5=format_float(height_vect[1], 10),
        p6=format_float(height_vect[2], 10),
        p7=format_float(cylinder.radius_bottom, 10),
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
    )


@ dataclass
class Zone():
    """Dataclass mapping for SH12A zones."""

    uuid: str

    id: int = 1
    figures_operators: list[set[int]] = field(default_factory=lambda: [{1}])
    material: str = "0"

    zone_template: str = """
  {id:03d}       {operators}"""

    def __str__(self) -> str:
        return self.zone_template.format(
            id=self.id,
            operators='OR'.join(['  '.join(['{0:+5}'.format(id)
                                 for id in figure_set])
                                 for figure_set in self.figures_operators]),
        )


@ dataclass
class GeoMatConfig:
    """Class mapping of the geo.dat config file."""

    figures: list[SolidFigure] = field(default_factory=lambda: [
        CylinderFigure(
            position=(0., 0., 10.),
            radius_top=10.,
            radius_bottom=10.,
            height=20.,
            rotation=(90., 0., 0.)
        ),
        CylinderFigure(
            position=(0., 0., 7.5),
            radius_top=15.,
            radius_bottom=15.,
            height=25.,
            rotation=(90., 0., 0.)
        ),
        CylinderFigure(
            position=(0., 0., 5.),
            radius_top=20.,
            radius_bottom=20.,
            height=30.,
            rotation=(90., 0., 0.)
        ),
    ]
    )
    zones: list[Zone] = field(default_factory=lambda: [
        Zone(
            uuid="",
            id=1,
            figures_operators=[{1, }],
            material="1",
        ),
        Zone(
            uuid="",
            id=2,
            figures_operators=[{-1, 2}],
            material="1000",
        ),
        Zone(
            uuid="",
            id=3,
            figures_operators=[{-2, 3}],
            material="0",
        ),
    ]
    )
    materials: list[tuple[str, str]] = field(default_factory=lambda: [("", 276)])
    jdbg1: int = 0
    jdbg2: int = 0
    title: str = "Unnamed geometry"

    material_template: str = """MEDIUM {idx:d}
ICRU {mat}
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
            # we increment idx because shieldhit indexes from 1 while python indexes lists from 0
            figures="".join([parse_figure(figure, idx+1) for idx, figure in enumerate(self.figures)])[1:],
            zones_geometries="".join([str(zone) for zone in self.zones])[1:],
            zones_materials=self._get_zone_material_string(),
        )

    def get_mat_string(self) -> str:
        """Generate mat.dat config."""
        # we increment idx because shieldhit indexes from 1 while python indexes lists from 0
        material_strings = [
            self.material_template.format(idx=idx+1, mat=mat[1])for idx, mat in enumerate(self.materials)]
        return "".join(material_strings)
