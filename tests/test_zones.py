import pytest
from converter.shieldhit.zones import SolidFigureParser, Zone
from converter import solid_figures

_Box_test_cases = {
    "case1": ({
        "uuid": "CBE326F9-48BB-4E5D-83CC-4F85B057AE00",
                "userData": {
                    "id": 941,
                    "geometryType": "BoxGeometry",
                    "position": [1, 2, 3],
                    "rotation": [45, 60, 90],
                    "parameters": {
                        "width": 1,
                        "height": 1,
                        "depth": 1
                    }
                },
    }, """
    TODO
    """),
}

_Cylinder_test_cases = {
    "case1": ({
        "uuid": "3A594908-17F2-4858-A16E-EE20BD387C26",
                "userData": {
                    "id": 940,
                    "geometryType": "CylinderGeometry",
                    "position": [1, 2, 3],
                    "rotation": [45, 60, 90],
                    "parameters": {
                        "radiusTop": 1,
                        "radiusBottom": 1,
                        "height": 1
                    }
                },
    }, """
    TODO
    """),
}

_Sphere_test_cases = {
    "case1": ({
        "uuid": "B0568AB3-A8F8-4615-8FF1-6121B506456F",
                "userData": {
                    "id": 1113,
                    "geometryType": "SphereGeometry",
                    "position": [1, 2, 3],
                    "rotation": [45, 60, 90],
                    "parameters": {
                        "radius": 1
                    }
                },
    }, """
    TODO
    """),
}


@pytest.fixture
def figure(request):
    """Fixture that provides a figure based on a json that contains figure information."""
    return solid_figures.parse_figure(request.param)


@pytest.mark.parametrize("figure,expected", _Box_test_cases, indirect=["figure"])
def test_box_parser(figure, expected):
    assert SolidFigureParser.parse(figure) == expected


@pytest.mark.parametrize("figure,expected", _Cylinder_test_cases, indirect=["figure"])
def test_cylinder_parser(figure, expected):
    assert SolidFigureParser.parse(figure) == expected


@pytest.mark.parametrize("figure,expected", _Sphere_test_cases, indirect=["figure"])
def test_cylinder_parser(figure, expected):
    assert SolidFigureParser.parse(figure) == expected


@pytest.fixture
def zone(request):
    """Fixture that provides a zone based on a json that contains zone information"""
    pass
