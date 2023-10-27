import logging
from converter import solid_figures
from converter.fluka.helper_parsers.figure_parser import FlukaCylinder, FlukaBox, FlukaSphere, parse_box, parse_cylinder, parse_sphere
import pytest
from tests.fluka.conftest import project_fluka_json

@pytest.fixture(scope='module')
def box_dict(project_fluka_json):
    """Part of the project.json file with the box figure"""
    return project_fluka_json['figureManager']['figures'][0]

@pytest.fixture(scope='module')
def cylinder_dict(project_fluka_json):
    """Part of the project.json file with the cylinder figure"""
    return project_fluka_json['figureManager']['figures'][1]

@pytest.fixture(scope='module')
def sphere_dict(project_fluka_json):
    """Part of the project.json file with the sphere figure"""
    return project_fluka_json['figureManager']['figures'][2]


def test_parse_cylinder(cylinder_dict):
    cylinder = solid_figures.CylinderFigure(uuid='ed1507a5-0489-4dc3-bb87-7b27dcff43e7',
                                          name='Cylinder',
                                          position=(2.14, 1.32, 0),
                                          rotation=(19.6, 14.2, 0),
                                          radius_top=1,
                                          radius_bottom=1,
                                          height=1)
    
    expected_fluka_cylinder = FlukaCylinder(figure_type = "RCC",
                                            name = "Cylinder",
                                            uuid = "ed1507a5-0489-4dc3-bb87-7b27dcff43e7",
                                            coordinates = [0, 0, 0],
                                            height_vector = [0, 0, 0],
                                            radius = 0)
    

    assert parse_cylinder(cylinder) == expected_fluka_cylinder

def test_parse_sphere():
    figure = solid_figures.SphereFigure(uuid='ed1507a5-0489-4dc3-bb87-7b27dcff43e7',
                                        name='Sphere',
                                        position=(2.14, 1.32, 0),
                                        radius=1)
    logging.warn(parse_sphere(figure))

def test_parse_box():
    figure = solid_figures.BoxFigure(uuid='ed1507a5-0489-4dc3-bb87-7b27dcff43e7',
                                     name='Box',
                                     position=(2.14, 1.32, 0),
                                     rotation=(19.6, 14.2, 0),
                                     x_edge_length=1,
                                     y_edge_length=1,
                                     z_edge_length=1)
    logging.warn(parse_box(figure))