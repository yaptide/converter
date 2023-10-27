from dataclasses import dataclass
from converter import solid_figures
from converter.solid_figures import BoxFigure, CylinderFigure, SolidFigure, SphereFigure
from scipy.spatial.transform import Rotation as R

@dataclass(frozen=False)
class FlukaFigure:
    figure_type: str = ""
    name: str = ""
    uuid: str = ""

@dataclass(frozen=False)
class FlukaBox(FlukaFigure):
    figure_type: str = "BOX"
    coordinates: list[float] = [0, 0, 0]
    x_vector: list[float] = [0, 0, 0]
    y_vector: list[float] = [0, 0, 0]
    z_vector: list[float] = [0, 0, 0]

@dataclass(frozen=False)
class FlukaCylinder(FlukaFigure):
    figure_type: str = "RCC"
    coordinates: list[float] = [0, 0, 0]
    height_vector: list[float] = [0, 0, 0]
    radius: float = 0

@dataclass(frozen=False)
class FlukaSphere(FlukaFigure):
    figure_type: str = "SPH"
    coordinates: list[float] = [0, 0, 0]
    radius: float = 0

def parse_box(box: BoxFigure) -> FlukaBox:
    """Parse box to Fluka box"""
    rotation = R.from_euler('xyz', box.rotation, degrees=True)
    x_vec = rotation.apply([box.x_edge_length, 0, 0])
    y_vec = rotation.apply([0, box.y_edge_length, 0])
    z_vec = rotation.apply([0, 0, box.z_edge_length])
    diagonal_vec = x_vec + y_vec + z_vec

    fluka_box = FlukaBox()
    fluka_box.coordinates = [
        box.position[0] - diagonal_vec[0] / 2,
        box.position[1] - diagonal_vec[1] / 2,
        box.position[2] - diagonal_vec[2] / 2,
    ]
    fluka_box.x_vector = x_vec
    fluka_box.y_vector = y_vec
    fluka_box.z_vector = z_vec
    fluka_box.uuid = box.uuid

    return fluka_box

def parse_cylinder(cylinder: CylinderFigure) -> FlukaCylinder:
    """Parse cylinder to Fluka cylinder"""
    rotation = R.from_euler('xyz', cylinder.rotation, degrees=True)
    height_vector = rotation.apply([0, 0, cylinder.height])

    fluka_cylinder = FlukaCylinder()
    fluka_cylinder.coordinates= [
        cylinder.position[0] - height_vector[0] / 2,
        cylinder.position[1] - height_vector[1] / 2,
        cylinder.position[2] - height_vector[2] / 2,
    ]
    fluka_cylinder.height_vector = height_vector
    fluka_cylinder.radius = cylinder.radius_top
    fluka_cylinder.uuid = cylinder.uuid

    return fluka_cylinder

def parse_sphere(sphere: SphereFigure) -> FlukaSphere:
    """Parse sphere to Fluka sphere"""
    fluka_sphere = FlukaSphere()
    fluka_sphere.radius = sphere.radius
    fluka_sphere.coordinates = [coord for coord in sphere.position]
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
        raise ValueError(f"Unexpected solid figure type: {figure}")
    
    return fluka_figure

def parse_figures(figures_json) -> list[FlukaFigure]:
    """Parse figures data from JSON to figures data used by Fluka"""
    raw_figures = [
            solid_figures.parse_figure(figure_dict) for figure_dict in figures_json
        ]
    
    fluka_figures = []
    figure_name = "fig{}"

    for idx, figure in raw_figures:
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