from converter.fluka.helper_parsers.figure_parser import parse_figures
from converter.fluka.helper_parsers.region_parser import BoolOperation, parse_regions
import pytest
import logging

@pytest.fixture(scope='module')
def zones_json(project_fluka_json):
    """zoneManager part of Fluka project.json file"""
    return project_fluka_json['zoneManager']

def test_parse_regions(zones_json, project_fluka_json):
    """Test if regions are parsed correctly"""
    
    figures = parse_figures(project_fluka_json["figureManager"].get('figures'))

    regions, _ = parse_regions(zones_json, figures)

    assert regions[0].name == "region0"
    assert regions[0].figures_operators == [[(BoolOperation.INTERSECTION, "fig0"), (BoolOperation.INTERSECTION, "fig1")]]

    assert regions[1].name == "region1"
    assert regions[1].figures_operators == [[(BoolOperation.INTERSECTION, "fig2"), (BoolOperation.INTERSECTION, "fig1")]]

    assert regions[2].name == "world"
    assert regions[2].figures_operators == [[(BoolOperation.INTERSECTION, "figworld"), (BoolOperation.SUBTRACTION, "fig0"), (BoolOperation.SUBTRACTION, "fig1"), (BoolOperation.SUBTRACTION, "fig2")]]

    assert regions[3].name == "boundary"
    assert regions[3].figures_operators == [[(BoolOperation.INTERSECTION, "figbound"), (BoolOperation.SUBTRACTION, "figworld")]]

    # ([FlukaRegion(name='region0', figures_operators=[[(<BoolOperation.INTERSECTION: 1>, 'fig0'), (<BoolOperation.INTERSECTION: 1>, 'fig1')]]), FlukaRegion(name='region1', figures_operators=[[(<BoolOperation.INTERSECTION: 1>, 'fig2'), (<BoolOperation.INTERSECTION: 1>, 'fig1')]]), FlukaRegion(name='world', figures_operators=[(<BoolOperation.INTERSECTION: 1>, 'figworld'), (<BoolOperation.SUBTRACTION: 2>, 'fig0'), (<BoolOperation.SUBTRACTION: 2>, 'fig1'), (<BoolOperation.SUBTRACTION: 2>, 'fig2')]), FlukaRegion(name='boundary', figures_operators=[(<BoolOperation.INTERSECTION: 1>, 'figbound'), (<BoolOperation.SUBTRACTION: 2>, 'figworld')])], [FlukaBox(figure_type='BOX', name='figworld', uuid='e6df7756-ecdd-44b7-95e1-b75ce620599d', coordinates=(0.0, 0.0, 10.5), x_vector=(0.0, 0.0, 0.0), y_vector=(0.0, 0.0, 0.0), z_vector=(0.0, 0.0, 0.0)), FlukaBox(figure_type='BOX', name='figbound', uuid='e6df7756-ecdd-44b7-95e1-b75ce620599d', coordinates=(-1.0, 0.0, 10.5), x_vector=(2.0, 0.0, 0.0), y_vector=(0.0, 2.0, 0.0), z_vector=(0.0, 0.0, 2.0))])