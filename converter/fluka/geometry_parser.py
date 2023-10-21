from dataclasses import dataclass
from converter import solid_figures
from converter.solid_figures import BoxFigure, CylinderFigure, SphereFigure
from scipy.spatial.transform import Rotation as R

@dataclass
class FlukaFigure:
    figure_type = ""
    name = ""

@dataclass
class FlukaBox(FlukaFigure):
    figure_type = "BOX"
    coordinates = [0, 0, 0]
    x_vector = [0, 0, 0]
    y_vector = [0, 0, 0]
    z_vector = [0, 0, 0]

@dataclass
class FlukaCylinder(FlukaFigure):
    figure_type = "RCC"
    coordinates = [0, 0, 0]
    height_vector = [0, 0, 0]
    radius = 0

@dataclass
class FlukaSphere(FlukaFigure):
    figure_type = "SPH"
    coordinates = [0, 0, 0]
    radius = 0

def parse_box(box):
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

    return fluka_box

def parse_cylinder(cylinder):
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

    return fluka_cylinder

def parse_sphere(sphere):
    """Parse sphere to Fluka sphere"""
    fluka_sphere = FlukaSphere()
    fluka_sphere.radius = sphere.radius
    fluka_sphere.coordinates = [coord for coord in sphere.position]
    return fluka_sphere

def parse_figures(figures_json) -> list: #TODO: add names to figures
    """Parse figures data from JSON to figures data used by Fluka"""

    raw_figures = [
            solid_figures.parse_figure(figure_dict) for figure_dict in figures_json
        ]
    
    fluka_figures = []

    for figure in raw_figures:
        if type(figure) is BoxFigure:
            fluka_figures.append(parse_box(figure))
        elif type(figure) is CylinderFigure:
            fluka_figures.append(parse_cylinder(figure))
        elif type(figure) is SphereFigure:
            fluka_figures.append(parse_sphere(figure))
        else:
            raise ValueError(f"Unexpected solid figure type: {figure}")

    return fluka_figures


def parse_zones() -> list:
    """Parse zones data from JSON to zones data used by Fluka"""

    return []