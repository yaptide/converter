"""Tests for SHIELD-HIT12A quantity settings (Settings blocks in detect.dat).

The `primaries` quantity setting is no longer supported (see yaptide/converter#279).
Input JSON may still contain the `primaries` key (e.g. projects saved by older UI versions);
it must be accepted and ignored.
"""

import copy
from dataclasses import fields
from typing import Optional

import pytest

from converter.api import get_parser_from_str, run_parser
from converter.shieldhit.detect import QuantitySettings

WATER_MATERIAL_UUID = "49ce56b9-ee48-4640-88d4-bcfd660d8c0e"


def _settings_blocks(detect_dat: str) -> list[list[str]]:
    """Return all Settings blocks from detect.dat content, each as a list of stripped lines (header excluded).

    Blocks in detect.dat start with a non-indented keyword line (Geometry, Filter, Settings, Output)
    and continue with indented lines.
    """
    blocks: list[list[str]] = []
    current: Optional[list[str]] = None
    for line in detect_dat.splitlines():
        if not line.strip():
            continue
        if not line[0].isspace():
            current = [] if line.strip() == "Settings" else None
            if current is not None:
                blocks.append(current)
        elif current is not None:
            current.append(line.strip())
    return blocks


def _convert_detect(project: dict) -> str:
    """Run the full SHIELD-HIT12A conversion with a fresh parser and return the detect.dat content."""
    parser = get_parser_from_str("shieldhit")
    return run_parser(parser, copy.deepcopy(project))["detect.dat"]


def _project_with_first_quantity(project: dict, name: str, extra: dict) -> dict:
    """Copy of the project where the first quantity (keyword Dose, no filter) gets new name and extra keys."""
    project = copy.deepcopy(project)
    quantity = project["scoringManager"]["outputs"][0]["quantities"][0]
    assert quantity["keyword"] == "Dose"
    assert "filter" not in quantity
    quantity["name"] = name
    quantity.update(extra)
    return project


@pytest.mark.parametrize(
    "kwargs",
    [
        {},
        {"rescale": 2.0},
        {"offset": 1.5},
        {"material": 1},
        {"medium": "WATER"},
        {"rescale": 2.0, "offset": 1.5, "material": 1, "medium": "WATER"},
    ],
    ids=["name_only", "rescale", "offset", "material", "medium", "all"],
)
def test_quantity_settings_str_has_no_primaries(kwargs: dict) -> None:
    """Settings block never contains a Primaries line"""
    settings_str = str(QuantitySettings(name="Test", **kwargs))
    assert settings_str.startswith("Settings\n    Name Test")
    assert "Primaries" not in settings_str


def test_quantity_settings_has_no_primaries_field() -> None:
    """QuantitySettings has no primaries field nor template (intended API break)"""
    assert "primaries" not in {f.name for f in fields(QuantitySettings)}
    assert "primaries" not in QuantitySettings.settings_dict
    with pytest.raises(TypeError):
        QuantitySettings(name="Test", primaries=1000)


@pytest.mark.parametrize("primaries", [1000, None], ids=["value", "null"])
@pytest.mark.parametrize("name", ["Quantity", "Quantity_1", "Dose"])
def test_primaries_only_creates_no_settings(project_shieldhit_json: dict, name: str, primaries: Optional[int]) -> None:
    """Quantity with only primaries set (UI may also send null) has no settings and references no settings name"""
    project = _project_with_first_quantity(project_shieldhit_json, name, {"primaries": primaries})
    parser = get_parser_from_str("shieldhit")
    detect_dat = run_parser(parser, project)["detect.dat"]

    assert _settings_blocks(detect_dat) == []
    first_quantity = parser.detect_config.outputs[0].quantities[0]
    assert first_quantity.settings is None
    assert "\n    Quantity Dose  \n" in detect_dat


@pytest.mark.parametrize(
    "name,extra,expected_name,expected_lines",
    [
        (
            "Quantity_1",
            {"primaries": 1000, "rescale": 2.0},
            "Rescaled_Dose_Quantity_1",
            ["Rescale 2.0"],
        ),
        (
            "Quantity",
            {"primaries": 1000, "offset": 1.5},
            "Dose_Quantity",
            ["Offset 1.5"],
        ),
        (
            "Quantity",
            {"primaries": 1000, "medium": "WATER"},
            "Dose_Quantity_to_WATER",
            ["NKMedium WATER"],
        ),
        (
            "Quantity",
            {"primaries": 1000, "materialUuid": WATER_MATERIAL_UUID},
            "Dose_Quantity_to_water_liquid",
            ["Medium 1"],
        ),
        (
            "Quantity_7",
            {"primaries": 1000, "rescale": 2.0, "medium": "WATER"},
            "Rescaled_Dose_Quantity_7_to_WATER",
            ["Rescale 2.0", "NKMedium WATER"],
        ),
        (
            "Quantity",
            {"primaries": 1000, "rescale": 2.0, "materialUuid": WATER_MATERIAL_UUID},
            "Rescaled_Dose_Quantity_to_water_liquid",
            ["Rescale 2.0", "Medium 1"],
        ),
        (
            "My custom-name 1!",
            {"primaries": 1000, "rescale": 2.0},
            "Mycustomname1",
            ["Rescale 2.0"],
        ),
    ],
    ids=[
        "rescale",
        "offset",
        "medium",
        "material",
        "rescale_medium",
        "rescale_material",
        "custom_name",
    ],
)
def test_primaries_ignored_in_settings(
    project_shieldhit_json: dict, name: str, extra: dict, expected_name: str, expected_lines: list[str]
) -> None:
    """Primaries neither appears in Settings nor affects the generated settings name"""
    project = _project_with_first_quantity(project_shieldhit_json, name, extra)
    detect_dat = _convert_detect(project)

    assert _settings_blocks(detect_dat) == [[f"Name {expected_name}", *expected_lines]]
    assert f"\n    Quantity Dose  {expected_name}\n" in detect_dat

    extra_without_primaries = {key: value for key, value in extra.items() if key != "primaries"}
    project_without_primaries = _project_with_first_quantity(project_shieldhit_json, name, extra_without_primaries)
    assert detect_dat == _convert_detect(project_without_primaries)


@pytest.mark.parametrize(
    "extra",
    [
        {},
        {"rescale": 3.0},
        {"medium": "WATER"},
    ],
    ids=["no_other_settings", "rescale", "medium"],
)
def test_primaries_in_all_quantities_is_ignored(project_shieldhit_json: dict, extra: dict) -> None:
    """Injecting primaries into every quantity of the project does not change detect.dat"""
    project_without_primaries = copy.deepcopy(project_shieldhit_json)
    for output in project_without_primaries["scoringManager"]["outputs"]:
        for quantity in output.get("quantities", []):
            quantity.update(extra)
    project_with_primaries = copy.deepcopy(project_without_primaries)
    for output in project_with_primaries["scoringManager"]["outputs"]:
        for quantity in output.get("quantities", []):
            quantity["primaries"] = 1000

    detect_dat = _convert_detect(project_with_primaries)

    assert detect_dat == _convert_detect(project_without_primaries)
    assert all(not line.startswith("Primaries") for block in _settings_blocks(detect_dat) for line in block)
    if not extra:
        assert _settings_blocks(detect_dat) == []
