import pytest
from converter import solid_figures

@pytest.fixture(scope='module')
def cylinder_figure_dict(project_shieldhit_json):
    """Part of the project.json file with the cylinder figure"""
    return project_shieldhit_json['figureManager']['figures'][0]

def test_cylinder_figure(cylinder_figure_dict):
    """Test if the cylinder figure is parsed correctly"""
    assert cylinder_figure_dict['type'] == 'CylinderFigure'
    assert cylinder_figure_dict['name'] == 'Water_phantom_cylinder'
    assert 'geometryData' in cylinder_figure_dict

    cylinder_figure_obj = solid_figures.parse_figure(cylinder_figure_dict)
    assert isinstance(cylinder_figure_obj, solid_figures.CylinderFigure)
    assert cylinder_figure_obj.radius_top == 5
    assert cylinder_figure_obj.radius_bottom == 5
    assert cylinder_figure_obj.height == 20
    assert cylinder_figure_obj.name == cylinder_figure_dict['name']
    assert cylinder_figure_obj.rotation[0] == cylinder_figure_dict['geometryData']['rotation'][0]
    assert cylinder_figure_obj.rotation[1] == cylinder_figure_dict['geometryData']['rotation'][1]
    assert cylinder_figure_obj.rotation[2] == cylinder_figure_dict['geometryData']['rotation'][2]
    assert cylinder_figure_obj.position[0] == cylinder_figure_dict['geometryData']['position'][0]
    assert cylinder_figure_obj.position[1] == cylinder_figure_dict['geometryData']['position'][1]
    assert cylinder_figure_obj.position[2] == cylinder_figure_dict['geometryData']['position'][2]
