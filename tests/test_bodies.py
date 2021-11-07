import pytest
from converter import bodies


_Json_with_bodies = {
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

_Cylinder_json = _Json_with_bodies["object"]["children"][0]
_Box_json = _Json_with_bodies["object"]["children"][1]
_Sphere_json = _Json_with_bodies["object"]["children"][2]


@pytest.fixture
def body(request):
    return bodies.parse_body(request.param)


@pytest.mark.parametrize("body,expected", [
    (_Cylinder_json, bodies.CylinderBody),
    (_Box_json, bodies.BoxBody),
    (_Sphere_json, bodies.SphereBody)
], indirect=["body"])
def test_type(body, expected):
    assert expected == type(body)


@pytest.mark.parametrize("body,expected", [
    (_Cylinder_json, _Cylinder_json),
    (_Box_json, _Box_json),
    (_Sphere_json, _Sphere_json)
], indirect=["body"])
def test_uuid(body, expected):
    assert expected['userData']['uuid'] == body.uuid


@pytest.mark.parametrize("body,expected", [
    (_Cylinder_json, _Cylinder_json),
    (_Box_json, _Box_json),
    (_Sphere_json, _Sphere_json)
], indirect=["body"])
def test_offset(body, expected):
    assert expected['userData']['position'] == [body.x_offset, body.y_offset, body.z_offset]


@pytest.mark.parametrize("body,expected", [
    (_Cylinder_json, _Cylinder_json),
    (_Box_json, _Box_json),
    (_Sphere_json, _Sphere_json)
], indirect=["body"])
def test_rotation(body, expected):
    assert expected['userData']['rotation'] == [body.x_rotation, body.y_rotation, body.z_rotation]
