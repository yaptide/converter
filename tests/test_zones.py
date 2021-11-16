import pytest
from converter.shieldhit.geo import Zone, parse_figure
from converter import solid_figures

_Box_test_cases = [
    ({
        "uuid": "CBE326F9-48BB-4E5D-83CC-4F85B057AE00",
                "userData": {
                    "id": 941,
                    "geometryType": "BoxGeometry",
                    "position": [1, 2, 3],
                    "rotation": [0, 0, 0],
                    "parameters": {
                        "width": 1,
                        "height": 1,
                        "depth": 1
                    }
                },
    }, """
  BOX    1       0.5       1.5       2.5       1.0       0.0       0.0
                 0.0       1.0       0.0       0.0       0.0       1.0"""),
]

_Cylinder_test_cases = [
    ({
        "uuid": "3A594908-17F2-4858-A16E-EE20BD387C26",
                "userData": {
                    "id": 940,
                    "geometryType": "CylinderGeometry",
                    "position": [1, 2, 3],
                    "rotation": [0, 0, 0],
                    "parameters": {
                        "radiusTop": 1,
                        "radiusBottom": 1,
                        "height": 1
                    }
                },
    }, """
  TRC    1       1.0       1.5       3.0       0.0       1.0       0.0
                 1.0       1.0                                        """)
]

_Sphere_test_cases = [
    ({
        "uuid": "B0568AB3-A8F8-4615-8FF1-6121B506456F",
                "userData": {
                    "id": 1113,
                    "geometryType": "SphereGeometry",
                    "position": [1, 2, 3],
                    "rotation": [0, 0, 0],
                    "parameters": {
                        "radius": 1
                    }
                },
    }, """
  SPH    1       1.0       2.0       3.0       1.0                    """),
]


@pytest.fixture
def figure(request):
    """Fixture that provides a figure based on a json that contains figure information."""
    return solid_figures.parse_figure(request.param)


@pytest.mark.parametrize("figure,expected", _Box_test_cases, indirect=["figure"])
def test_box_parser(figure, expected):
    """Test if boxes are parsed corectly."""
    assert parse_figure(figure, 1) == expected


@pytest.mark.parametrize("figure,expected", _Cylinder_test_cases, indirect=["figure"])
def test_cylinder_parser(figure, expected):
    """Test if cylinders are parsed corectly."""
    assert parse_figure(figure, 1) == expected


@pytest.mark.parametrize("figure,expected", _Sphere_test_cases, indirect=["figure"])
def test_sphere_parser(figure, expected):
    """Test if spheres are parsed corectly."""
    assert parse_figure(figure, 1) == expected


_Zone_test_cases = [
    (
        {
            "id": 1,
            "figures_operators": [{1}],
        },
        """
  001          +1                                                        """
    ),
    (
        {
            "id": 11,
            "figures_operators": [{-2}],
        },
        """
  011          -2                                                        """
    ),
    (
        {
            "id": 111,
            "figures_operators": [{1, -2}],
        },
        """
  111          +1     -2                                                 """
    ),
    (
        {
            "id": 2,
            "figures_operators": [{1}, {-2}],
        },
        """
  002          +1OR   -2                                                 """
    ),
    (
        {
            "id": 3,
            "figures_operators": [{1, -2}, {11, -12, 13}],
        },
        """
  003          +1     -2OR  +11    -12    +13                            """
    ),
    (
        {
            "id": 4,
            "figures_operators": [{4, -2}, {2}, {3, 4}],
        },
        """
  004          +4     -2OR   +2OR   +3     +4                            """
    )
]


@pytest.fixture
def zone(request):
    """
    Fixture that provides a zone based on a list containing csg information, id
    and material that the zone is made out of.
    """
    return Zone(**request.param)


@pytest.mark.parametrize("zone,expected", _Zone_test_cases, indirect=["zone"])
def test_zones(zone, expected):
    """Test if zone string representation is correct"""
    assert str(zone) == expected
