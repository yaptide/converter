from converter.fluka.helper_parsers.material_parser import (
    parse_materials,
    assign_materials_to_regions,
)
import pytest


@pytest.fixture(scope="module")
def zones_json(project_fluka_json):
    """zoneManager part of Fluka project.json file"""
    return project_fluka_json["zoneManager"]


@pytest.fixture(scope="module")
def materials_json(project_fluka_json):
    """materialManager part of Fluka project.json file"""
    return project_fluka_json["materialManager"]["materials"]


def test_parse_materials(zones_json, materials_json):
    """Test if materials are parsed correctly"""

    materials, compounds = parse_materials(materials_json, zones_json)

    assert "c68fba8d-e146-44df-96f8-f6ab74d48cfa" in materials
    assert "fdd9632f-5e37-4952-81a8-a01d1b9c2842" in materials
    assert "9dd76291-d711-4838-bf8f-a7695f5344e1" in materials
    assert "a0a41c8b-9c22-42b6-bbfa-a6bad91d088d" in materials

    assert materials["c68fba8d-e146-44df-96f8-f6ab74d48cfa"].density == 0.00120479
    assert materials["fdd9632f-5e37-4952-81a8-a01d1b9c2842"].density == 1.01
    assert materials["9dd76291-d711-4838-bf8f-a7695f5344e1"].density == 11.36
    assert materials["a0a41c8b-9c22-42b6-bbfa-a6bad91d088d"].density == 1

    assert "fdd9632f-5e37-4952-81a8-a01d1b9c2842" in compounds
