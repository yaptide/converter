import pytest
from converter.shieldhit.geo import Zone

@pytest.fixture(scope='module')
def water_phantom_zone_dict(project_shieldhit_json):
    """Part of the project.json file with the water phantom zone"""
    return project_shieldhit_json['zoneManager']['zones'][0]

def test_water_phantom_zone(water_phantom_zone_dict):
    assert water_phantom_zone_dict['name'] == 'Water_phantom_zone'
    zone_obj = Zone(water_phantom_zone_dict)
    assert zone_obj.id == 1
    assert zone_obj.material == 0 # why ???
    assert str(zone_obj) == '\n  001          +1'
