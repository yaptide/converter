import logging
import math
from converter import solid_figures
from converter.fluka.helper_parsers.figure_parser import FlukaCylinder, FlukaBox, FlukaSphere, parse_box, parse_cylinder, parse_sphere
import pytest

def test_parse_cylinder():
    cylinder = solid_figures.CylinderFigure(uuid='ed1507a5-0489-4dc3-bb87-7b27dcff43e7',
                                          name='Cylinder',
                                          position=(2.14, 1.32, 0),
                                          rotation=(19.6, 14.2, 0),
                                          radius_top=1,
                                          radius_bottom=1,
                                          height=1)

    fluka_cylinder = parse_cylinder(cylinder)

    assert fluka_cylinder.figure_type == "RCC"
    assert fluka_cylinder.uuid == "ed1507a5-0489-4dc3-bb87-7b27dcff43e7"
    assert all(math.isclose(a, b, abs_tol=1e-8) for a, b in zip(fluka_cylinder.coordinates,
                                                                (2.0244531744545524, 1.4877257848751275, -0.45663660846935195)))
    assert all(math.isclose(a, b, abs_tol=1e-8) for a, b in zip(fluka_cylinder.height_vector,
                                                                (0.23109365, -0.33545157, 0.91327322)))
    assert fluka_cylinder.radius == 1

def test_parse_sphere():
    sphere = solid_figures.SphereFigure(uuid='ed1507a5-0489-4dc3-bb87-7b27dcff43e7',
                                        name='Sphere',
                                        position=(2.14, 1.32, 0),
                                        radius=1)

    fluka_sphere = parse_sphere(sphere)

    assert fluka_sphere.figure_type == "SPH"
    assert fluka_sphere.uuid == "ed1507a5-0489-4dc3-bb87-7b27dcff43e7"
    assert all(math.isclose(a, b, abs_tol=1e-8) for a, b in zip(fluka_sphere.coordinates,
                                                                (2.14, 1.32, 0)))
    assert fluka_sphere.radius == 1

def test_parse_box():
    figure = solid_figures.BoxFigure(uuid='ed1507a5-0489-4dc3-bb87-7b27dcff43e7',
                                     name='Box',
                                     position=(2.14, 1.32, 0),
                                     rotation=(19.6, 14.2, 0),
                                     x_edge_length=1,
                                     y_edge_length=1,
                                     z_edge_length=1)

    fluka_box = parse_box(figure)

    assert fluka_box.figure_type == "BOX"
    assert fluka_box.uuid == "ed1507a5-0489-4dc3-bb87-7b27dcff43e7"
    assert all(math.isclose(a, b, abs_tol=1e-8) for a, b in zip(fluka_box.coordinates,
                                                                (1.65527732505, 1.32, 0.1226536929)))
    assert all(math.isclose(a, b, abs_tol=1e-8) for a, b in zip(fluka_box.x_vector,
                                                                (0.96944534989, 6.9388939e-18, -0.24530738587)))
    assert all(math.isclose(a, b, abs_tol=1e-8) for a, b in zip(fluka_box.y_vector,
                                                                (0.08228874766, 0.94205745278, 0.32520196440)))
    assert all(math.isclose(a, b, abs_tol=1e-8) for a, b in zip(fluka_box.z_vector,
                                                                (0.23109365109, -0.3354515697, 0.91327321693)))