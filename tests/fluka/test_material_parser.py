from converter.fluka.helper_parsers.material_parser import (
    parse_materials,
    assign_materials_to_regions,
)
from converter.fluka.helper_parsers.figure_parser import parse_figures
from converter.fluka.helper_parsers.region_parser import parse_regions
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
    materials, compounds, _ = parse_materials(materials_json, zones_json)

    assert "c68fba8d-e146-44df-96f8-f6ab74d48cfa" in materials
    assert "fdd9632f-5e37-4952-81a8-a01d1b9c2842" in materials
    assert "9dd76291-d711-4838-bf8f-a7695f5344e1" in materials
    assert "a0a41c8b-9c22-42b6-bbfa-a6bad91d088d" in materials

    assert materials["c68fba8d-e146-44df-96f8-f6ab74d48cfa"].density == 0.00120479
    assert materials["fdd9632f-5e37-4952-81a8-a01d1b9c2842"].density == 1.01
    assert materials["9dd76291-d711-4838-bf8f-a7695f5344e1"].density == 11.36
    assert materials["a0a41c8b-9c22-42b6-bbfa-a6bad91d088d"].density == 1

    assert "fdd9632f-5e37-4952-81a8-a01d1b9c2842" in compounds


def test_assign_materials_to_regions(zones_json, materials_json, project_fluka_json):
    """Test if materials are assigned to regions correctly"""
    materials, _, _ = parse_materials(materials_json, zones_json)
    figures = parse_figures(project_fluka_json["figureManager"].get("figures"))
    regions, _ = parse_regions(zones_json, figures)

    assignments = assign_materials_to_regions(materials, regions, zones_json)

    assert len(assignments) == len(regions)

    assert assignments[0].region_name == "region0"
    assert assignments[0].material_name == "AIR"
    assert assignments[1].region_name == "region1"
    assert assignments[1].material_name == "COM00001"
    assert assignments[2].region_name == "region2"
    assert assignments[2].material_name == "MAT00001"
    assert assignments[3].region_name == "region3"
    assert assignments[3].material_name == "AIR"
    assert assignments[4].region_name == "world"
    assert assignments[4].material_name == "WATER"
    assert assignments[5].region_name == "boundary"
    assert assignments[5].material_name == "BLCKHOLE"
