from dataclasses import dataclass, field
from converter import solid_figures
from converter.solid_figures import BoxFigure, CylinderFigure, SolidFigure, SphereFigure
from converter.common import rotate


@dataclass(frozen=False)
class FlukaFigure:
    """Abstract class representing Fluka figure"""

    figure_type: str = ''
    name: str = ''
    uuid: str = ''


@dataclass(frozen=False)
class FlukaBox(FlukaFigure):
    """Class representing Fluka box"""

    figure_type: str = 'RPP'
    x_min: float = 0
    x_max: float = 0
    y_min: float = 0
    y_max: float = 0
    z_min: float = 0
    z_max: float = 0


@dataclass(frozen=False)
class FlukaCylinder(FlukaFigure):
    """Class representing Fluka cylinder"""

    figure_type: str = 'RCC'
    coordinates: list[float] = field(default_factory=lambda: (0, 0, 0))
    height_vector: list[float] = field(default_factory=lambda: (0, 0, 0))
    radius: float = 0
    rotation: list[float] = field(default_factory=lambda: (0, 0, 0))
    height: float = 0


@dataclass(frozen=False)
class FlukaSphere(FlukaFigure):
    """Class representing Fluka sphere"""

    figure_type: str = 'SPH'
    coordinates: list[float] = field(default_factory=lambda: (0, 0, 0))
    radius: float = 0


def parse_box(box: BoxFigure) -> FlukaBox:
    """
    Parse box to Fluka RPP.
    RPP is a parallelepiped with sides parallel to the coordinate axes.
    In case the box to parse has rotation applied, we throw an error.
    """
    if (box.rotation[0] != 0 or box.rotation[1] != 0 or box.rotation[2] != 0):
        raise ValueError('Rotation of box is not supported for Fluka')

    fluka_box = FlukaBox()
    fluka_box.uuid = box.uuid
    fluka_box.x_min = box.position[0] - box.x_edge_length / 2
    fluka_box.x_max = box.position[0] + box.x_edge_length / 2
    fluka_box.y_min = box.position[1] - box.y_edge_length / 2
    fluka_box.y_max = box.position[1] + box.y_edge_length / 2
    fluka_box.z_min = box.position[2] - box.z_edge_length / 2
    fluka_box.z_max = box.position[2] + box.z_edge_length / 2

    return fluka_box


def parse_cylinder(cylinder: CylinderFigure) -> FlukaCylinder:
    """Parse cylinder to Fluka cylinder"""
    height_vector = rotate((0, 0, cylinder.height), cylinder.rotation)

    fluka_cylinder = FlukaCylinder()
    fluka_cylinder.coordinates = (
        cylinder.position[0] - height_vector[0] / 2,
        cylinder.position[1] - height_vector[1] / 2,
        cylinder.position[2] - height_vector[2] / 2,
    )
    fluka_cylinder.height_vector = height_vector
    fluka_cylinder.radius = cylinder.radius_top
    fluka_cylinder.uuid = cylinder.uuid
    fluka_cylinder.rotation = cylinder.rotation
    fluka_cylinder.height = cylinder.height

    return fluka_cylinder


def parse_sphere(sphere: SphereFigure) -> FlukaSphere:
    """Parse sphere to Fluka sphere"""
    fluka_sphere = FlukaSphere()
    fluka_sphere.radius = sphere.radius
    fluka_sphere.coordinates = (sphere.position[0], sphere.position[1], sphere.position[2])
    fluka_sphere.uuid = sphere.uuid
    return fluka_sphere


def parse_fluka_figure(figure: SolidFigure) -> FlukaFigure:
    """Parse any SolidFigure to FlukaFigure"""
    if type(figure) is BoxFigure:
        fluka_figure = parse_box(figure)
    elif type(figure) is CylinderFigure:
        fluka_figure = parse_cylinder(figure)
    elif type(figure) is SphereFigure:
        fluka_figure = parse_sphere(figure)
    else:
        raise ValueError(f'Unexpected solid figure type: {figure}')

    return fluka_figure


def parse_figures(figures_json) -> list[FlukaFigure]:
    """Parse figures data from JSON to figures data used by Fluka"""
    raw_figures = [solid_figures.parse_figure(figure_dict) for figure_dict in figures_json]

    fluka_figures = []
    figure_name = 'fig{}'

    for idx, figure in enumerate(raw_figures):
        fluka_figure = parse_fluka_figure(figure)
        fluka_figure.name = figure_name.format(idx)
        fluka_figures.append(fluka_figure)

    return fluka_figures


def get_figure_name_by_uuid(figures_list: list[FlukaFigure], uuid: str) -> str:
    """Helper function which returns name of figure with provided uuid"""
    for figure in figures_list:
        if figure.uuid == uuid:
            return figure.name
    return None
