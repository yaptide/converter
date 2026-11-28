import math
from converter import solid_figures
from converter.fluka.helper_parsers.figure_parser import parse_box, parse_cylinder, parse_sphere


def test_parse_cylinder():
    """Test if cylinder is parsed correctly"""
    cylinder = solid_figures.CylinderFigure(
        uuid="ed1507a5-0489-4dc3-bb87-7b27dcff43e7",
        name="Cylinder",
        position=(2.14, 1.32, 0),
        rotation=(19.6, 14.2, 0),
        radius_top=1,
        radius_bottom=1,
        height=1,
    )

    fluka_cylinder = parse_cylinder(cylinder)

    # expected values computed with three.js (Euler 'XYZ'), as the editor orients the cylinder

    assert fluka_cylinder.figure_type == "RCC"
    assert fluka_cylinder.uuid == "ed1507a5-0489-4dc3-bb87-7b27dcff43e7"
    assert all(
        math.isclose(a, b, abs_tol=1e-8)
        for a, b in zip(fluka_cylinder.coordinates, (2.0173463071, 1.4826009822, -0.4566366085))
    )
    assert all(
        math.isclose(a, b, abs_tol=1e-8)
        for a, b in zip(fluka_cylinder.height_vector, (0.2453073859, -0.3252019644, 0.9132732169))
    )
    assert fluka_cylinder.radius == 1


def test_parse_sphere():
    """Test if sphere is parsed correctly"""
    sphere = solid_figures.SphereFigure(
        uuid="ed1507a5-0489-4dc3-bb87-7b27dcff43e7", name="Sphere", position=(2.14, 1.32, 0), radius=1
    )

    fluka_sphere = parse_sphere(sphere)

    assert fluka_sphere.figure_type == "SPH"
    assert fluka_sphere.uuid == "ed1507a5-0489-4dc3-bb87-7b27dcff43e7"
    assert all(math.isclose(a, b, abs_tol=1e-8) for a, b in zip(fluka_sphere.coordinates, (2.14, 1.32, 0)))
    assert fluka_sphere.radius == 1


def test_parse_box():
    """Test if box is parsed correctly"""
    figure = solid_figures.BoxFigure(
        uuid="ed1507a5-0489-4dc3-bb87-7b27dcff43e7",
        name="Box",
        position=(2.14, 1.32, 0),
        rotation=(0, 0, 0),
        x_edge_length=1,
        y_edge_length=1,
        z_edge_length=1,
    )

    fluka_box = parse_box(figure)

    assert fluka_box.figure_type == "RPP"
    assert fluka_box.uuid == "ed1507a5-0489-4dc3-bb87-7b27dcff43e7"
    assert math.isclose(fluka_box.x_min, 1.64)
    assert math.isclose(fluka_box.x_max, 2.64)
    assert math.isclose(fluka_box.y_min, 0.82)
    assert math.isclose(fluka_box.y_max, 1.82)
    assert math.isclose(fluka_box.z_min, -0.5)
    assert math.isclose(fluka_box.z_max, 0.5)


def test_rotated_box():
    """A rotated box is written around the origin and keeps its rotation and position for ROT-DEFI"""
    figure = solid_figures.BoxFigure(
        uuid="ed1507a5-0489-4dc3-bb87-7b27dcff43e7",
        name="Box",
        position=(2.14, 1.32, 0),
        rotation=(1, 56, 76),
        x_edge_length=1,
        y_edge_length=2,
        z_edge_length=3,
    )

    fluka_box = parse_box(figure)

    assert fluka_box.figure_type == "RPP"
    assert fluka_box.is_rotated
    assert (fluka_box.x_min, fluka_box.x_max) == (-0.5, 0.5)
    assert (fluka_box.y_min, fluka_box.y_max) == (-1.0, 1.0)
    assert (fluka_box.z_min, fluka_box.z_max) == (-1.5, 1.5)
    assert fluka_box.rotation == (1, 56, 76)
    assert fluka_box.position == (2.14, 1.32, 0)
