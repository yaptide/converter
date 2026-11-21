from converter import solid_figures
from converter.fluka.cards.figure_card import FiguresCard
from converter.fluka.cards.transformation_card import TransformationsCard
from converter.fluka.helper_parsers.figure_parser import parse_box


def rotated_box():
    box = parse_box(
        solid_figures.BoxFigure(
            position=(3.0, -2.0, 1.0), rotation=(30, 40, 50), x_edge_length=10, y_edge_length=1, z_edge_length=1
        )
    )
    box.name = "fig0"
    return box


def test_rotated_box_is_placed_by_transformation():
    lines = str(FiguresCard(data=[rotated_box()])).splitlines()
    i = lines.index("$Start_transform -rotfig0")
    assert lines[i + 1].startswith("RPP fig0 -5.0 +5.0 -0.5 +0.5 -0.5 +0.5")
    assert lines[i + 2] == "$End_transform"


def test_rot_defi_cards():
    # rotations about X, Y, Z (WHAT(1) = 101, 201, 301); the first card translates by minus the position
    assert str(TransformationsCard(data=[rotated_box()])).splitlines() == [
        "* rotation and position of box fig0",
        "ROT-DEFI       101.0       0.0      30.0      -3.0       2.0      -1.0rotfig0",
        "ROT-DEFI       201.0       0.0      40.0                              rotfig0",
        "ROT-DEFI       301.0       0.0      50.0                              rotfig0",
    ]


def test_unrotated_box_has_no_transformation():
    box = parse_box(solid_figures.BoxFigure(position=(1.0, 2.0, 3.0), x_edge_length=2))
    box.name = "fig0"
    assert str(TransformationsCard(data=[box])) == ""
    assert "$Start_transform" not in str(FiguresCard(data=[box]))
