import pytest
from converter import solid_figures


_Json_with_figures = {
    "object": {
        "children": [
            {
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
            },
            {
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
            },
            {
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
            },
        ]
    }
}

_Cylinder_json = _Json_with_figures["object"]["children"][0]
_Box_json = _Json_with_figures["object"]["children"][1]
_Sphere_json = _Json_with_figures["object"]["children"][2]


@pytest.fixture
def figure(request):
    """Fixture that provides a figure based on a json that contains figure information."""
    return solid_figures.parse_figure(request.param)


@pytest.mark.parametrize("figure,expected", [
    (_Cylinder_json, solid_figures.CylinderFigure),
    (_Box_json, solid_figures.BoxFigure),
    (_Sphere_json, solid_figures.SphereFigure)
], indirect=["figure"])
def test_type(figure, expected):
    """Test if parser returns correct figure object type"""
    assert type(figure) is expected


@pytest.mark.parametrize("figure,expected", [
    (_Cylinder_json, _Cylinder_json),
    (_Box_json, _Box_json),
    (_Sphere_json, _Sphere_json)
], indirect=["figure"])
def test_uuid(figure, expected):
    """Test if figure_parser parses uuid correctly"""
    assert figure.uuid == expected['uuid']


@pytest.mark.parametrize("figure,expected", [
    (_Cylinder_json, _Cylinder_json),
    (_Box_json, _Box_json),
    (_Sphere_json, _Sphere_json)
], indirect=["figure"])
def test_offset(figure, expected):
    """Test if figure_parser parses offset(position) correctly"""
    assert figure.offset == tuple(expected['userData']['position'])


@pytest.mark.parametrize("figure,expected", [
    (_Cylinder_json, _Cylinder_json),
    (_Box_json, _Box_json),
    (_Sphere_json, _Sphere_json)
], indirect=["figure"])
def test_rotation(figure, expected):
    """Test if figure_parser parses rotation correctly"""
    assert figure.rotation == tuple(expected['userData']['rotation'])
