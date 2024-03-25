from typing import Optional
from converter.common import format_float, rotate
from converter.solid_figures import SolidFigure, BoxFigure, CylinderFigure, SphereFigure
from dataclasses import dataclass, field
from enum import IntEnum


class DefaultMaterial(IntEnum):
    """
    List of special material ids that are not referring to the `mat` and have a separate
    meaning. E.g. Assigning id=1000 to a zone in `geo` file would mean, that the zone is made out
    of vacuum, not that it refers to the 1000th item in `mat` file.
    """

    BLACK_HOLE = 0
    VACUUM = 1000

    @staticmethod
    def is_default_material(material_value: int) -> bool:
        """Check if the material is one of the predefined default materials."""
        return material_value in DefaultMaterial._value2member_map_


def parse_figure(figure: SolidFigure, number: int) -> str:
    """Parse a SolidFigure into a string representation of SH12A input file."""
    if type(figure) is BoxFigure:
        return _parse_box(figure, number)
    if type(figure) is CylinderFigure:
        return _parse_cylinder(figure, number)
    if type(figure) is SphereFigure:
        return _parse_sphere(figure, number)

    raise ValueError(f'Unexpected solid figure type: {figure}')


def _parse_box(box: BoxFigure, number: int) -> str:
    """Parse a BoxFigure into a str representation of SH12A input file."""
    x_vec = rotate([box.x_edge_length, 0, 0], box.rotation)
    y_vec = rotate([0, box.y_edge_length, 0], box.rotation)
    z_vec = rotate([0, 0, box.z_edge_length], box.rotation)
    diagonal_vec = x_vec + y_vec + z_vec
    start_position = (
        box.position[0] - diagonal_vec[0] / 2,
        box.position[1] - diagonal_vec[1] / 2,
        box.position[2] - diagonal_vec[2] / 2,
    )
    box_template = """
  BOX {number:>4}{p1:>10}{p2:>10}{p3:>10}{p4:>10}{p5:>10}{p6:>10}
          {p7:>10}{p8:>10}{p9:>10}{p10:>10}{p11:>10}{p12:>10}"""
    return box_template.format(
        number=number,
        p1=format_float(start_position[0], 10),
        p2=format_float(start_position[1], 10),
        p3=format_float(start_position[2], 10),
        p4=format_float(x_vec[0], 10),
        p5=format_float(x_vec[1], 10),
        p6=format_float(x_vec[2], 10),
        p7=format_float(y_vec[0], 10),
        p8=format_float(y_vec[1], 10),
        p9=format_float(y_vec[2], 10),
        p10=format_float(z_vec[0], 10),
        p11=format_float(z_vec[1], 10),
        p12=format_float(z_vec[2], 10),
    )


def _parse_cylinder(cylinder: CylinderFigure, number: int) -> str:
    """Parse a CylinderFigure into a str representation of SH12A input file."""

    height_vect = rotate([0, 0, cylinder.height], cylinder.rotation)
    lower_base_position = (
        cylinder.position[0] - height_vect[0] / 2,
        cylinder.position[1] - height_vect[1] / 2,
        cylinder.position[2] - height_vect[2] / 2,
    )
    rcc_template = """
  RCC {number:>4}{p1:>10}{p2:>10}{p3:>10}{p4:>10}{p5:>10}{p6:>10}
          {p7:>10}"""
    return rcc_template.format(
        number=number,
        p1=format_float(lower_base_position[0], 10),
        p2=format_float(lower_base_position[1], 10),
        p3=format_float(lower_base_position[2], 10),
        p4=format_float(height_vect[0], 10),
        p5=format_float(height_vect[1], 10),
        p6=format_float(height_vect[2], 10),
        p7=format_float(cylinder.radius_top, 10),
    )


def _parse_sphere(sphere: SphereFigure, number: int) -> str:
    """Parse a SphereFigure into a str representation of SH12A input file."""
    sphere_entry_template = """
  SPH {number:>4}{p1:>10}{p2:>10}{p3:>10}{p4:>10}"""
    return sphere_entry_template.format(
        number=number,
        p1=format_float(sphere.position[0], 10),
        p2=format_float(sphere.position[1], 10),
        p3=format_float(sphere.position[2], 10),
        p4=format_float(sphere.radius, 10),
    )


@dataclass
class Material:
    """Dataclass mapping for SH12A materials."""

    name: str
    sanitized_name: str
    uuid: str
    icru: int
    density: Optional[float] = None
    custom_stopping_power: bool = False
    idx: int = 0

    property_template = """{name} {value}\n"""
    property_template_name = """{name}\n"""

    def __str__(self) -> str:
        result = self.property_template.format(name='MEDIUM', value=self.idx)
        result += self.property_template.format(name='ICRU', value=self.icru)
        if self.density is not None:
            result += self.property_template.format(name='RHO', value=format_float(self.density, 10))

        if self.custom_stopping_power:
            result += self.property_template_name.format(name='LOADDEDX')

        result += 'END\n'
        return result


@dataclass
class Zone:
    """Dataclass mapping for SH12A zones."""

    uuid: str

    id: int = 1
    figures_operators: list[set[int]] = field(default_factory=lambda: [{1}])
    material: int = 0
    material_override: dict[str, str] = field(default_factory=dict)

    zone_template: str = """
  {id:03d}       {operators}"""

    def __str__(self) -> str:
        return self.zone_template.format(
            id=self.id,
            operators='OR'.join(['  '.join([f'{id:+5}' for id in figure_set])
                                 for figure_set in self.figures_operators]),
        )


@dataclass
class StoppingPowerFile:
    """Dataclass mapping for SH12A stopping power files."""

    icru: int
    name: str
    content: str


@dataclass
class GeoMatConfig:
    """Class mapping of the geo.dat config file."""

    figures: list[SolidFigure] = field(default_factory=lambda: [
        CylinderFigure(position=(0., 0., 10.), radius_top=10., radius_bottom=10., height=20., rotation=(90., 0., 0.)),
        CylinderFigure(position=(0., 0., 7.5), radius_top=15., radius_bottom=15., height=25., rotation=(90., 0., 0.)),
        CylinderFigure(position=(0., 0., 5.), radius_top=20., radius_bottom=20., height=30., rotation=(90., 0., 0.)),
    ])
    zones: list[Zone] = field(default_factory=lambda: [
        Zone(
            uuid='',
            id=1,
            figures_operators=[{
                1,
            }],
            material=1,
        ),
        Zone(
            uuid='',
            id=2,
            figures_operators=[{-1, 2}],
            material=1000,
        ),
        Zone(
            uuid='',
            id=3,
            figures_operators=[{-2, 3}],
            material=0,
        ),
    ])
    materials: list[Material] = field(default_factory=lambda: [Material('', '', '', 276)])
    jdbg1: int = 0
    jdbg2: int = 0
    title: str = 'Unnamed geometry'
    available_custom_stopping_power_files: dict[int, StoppingPowerFile] = field(default_factory=lambda: {})

    geo_template: str = """
{jdbg1:>5}{jdbg1:>5}          {title}
{figures}
  END
{zones_geometries}
  END
{zones_materials}
"""

    @staticmethod
    def _split_zones_to_rows(zones: list[int], max_size=14) -> list[list[int]]:
        """Split list of Zones into rows of not more than 14 elements"""
        return [zones[i:min(i + max_size, len(zones))] for i in range(0, len(zones), max_size)]

    def _get_zone_material_string(self) -> str:
        """Generate material_id, zone_id pairs string (for geo.dat)."""
        # Cut lists into chunks of max size 14
        zone_ids = [
            ''.join([f'{id:>5}' for id in row])
            for row in GeoMatConfig._split_zones_to_rows([zone.id for zone in self.zones])
        ]
        material_ids = [
            ''.join([f'{mat:>5}' for mat in row])
            for row in GeoMatConfig._split_zones_to_rows([zone.material for zone in self.zones])
        ]
        return '\n'.join([*zone_ids, *material_ids])

    def get_geo_string(self) -> str:
        """Generate geo.dat config."""
        return self.geo_template.format(
            jdbg1=self.jdbg1,
            jdbg2=self.jdbg2,
            title=self.title,
            # we increment idx because shieldhit indexes from 1 while python indexes lists from 0
            figures=''.join([parse_figure(figure, idx + 1) for idx, figure in enumerate(self.figures)])[1:],
            zones_geometries=''.join([str(zone) for zone in self.zones])[1:],
            zones_materials=self._get_zone_material_string(),
        )

    def get_mat_string(self) -> str:
        """Generate mat.dat config."""
        # we increment idx because shieldhit indexes from 1 while python indexes lists from 0
        material_strings = []
        materials_filtered = filter(lambda x: not DefaultMaterial.is_default_material(x.icru), self.materials)
        for idx, material in enumerate(materials_filtered):
            material.idx = idx + 1
            material_strings.append(str(material))

        return ''.join(material_strings)
