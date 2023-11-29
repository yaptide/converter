from converter.fluka.helper_parsers.figure_parser import parse_figures
from converter.fluka.helper_parsers.region_parser import BoolOperation, parse_regions
import pytest

@pytest.fixture(scope='module')
def zones_json(project_fluka_json):
    """zoneManager part of Fluka project.json file"""
    return project_fluka_json['zoneManager']

def test_parse_regions(zones_json, project_fluka_json):
    """Test if regions are parsed correctly"""
    figures = parse_figures(project_fluka_json["figureManager"].get('figures'))

    regions, _ = parse_regions(zones_json, figures)
    regions = list(regions.values())

    assert regions[0].name == "region0"
    assert regions[0].figures_operators == [[(BoolOperation.INTERSECTION, "fig0"), (BoolOperation.SUBTRACTION, "fig1"),
                                            (BoolOperation.SUBTRACTION, "fig2")]]

    assert regions[1].name == "region1"
    assert regions[1].figures_operators == [[(BoolOperation.INTERSECTION, "fig1")]]

    assert regions[2].name == "region2"
    assert regions[2].figures_operators == [[(BoolOperation.INTERSECTION, "fig2"), (BoolOperation.SUBTRACTION, "fig3")]]

    assert regions[3].name == "region3"
    assert regions[3].figures_operators == [[(BoolOperation.INTERSECTION, "fig3")]]

    assert regions[4].name == "world"
    assert regions[4].figures_operators == [[(BoolOperation.INTERSECTION, "figworld"), (BoolOperation.SUBTRACTION, "fig0"),
                                             (BoolOperation.SUBTRACTION, "fig1"), (BoolOperation.SUBTRACTION, "fig2"),
                                             (BoolOperation.SUBTRACTION, "fig3"), (BoolOperation.SUBTRACTION, "fig4")]]

    assert regions[5].name == "boundary"
    assert regions[5].figures_operators == [[(BoolOperation.INTERSECTION, "figbound"), (BoolOperation.SUBTRACTION, "figworld")]]