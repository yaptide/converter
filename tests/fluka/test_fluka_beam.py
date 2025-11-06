import copy
from math import isclose
from converter.fluka.helper_parsers.beam_parser import BeamShape, parse_beam


def test_parse_fluka_beam(project_fluka_json):
    """Test if Fluka beam is parsed correctly"""
    beam_json = project_fluka_json['beam']

    fluka_beam = parse_beam(beam_json)

    assert fluka_beam.energy_MeV == 70
    assert fluka_beam.particle_name == 'PROTON'
    assert fluka_beam.shape == BeamShape.CIRCULAR
    assert fluka_beam.shape_x == 0
    assert fluka_beam.shape_y == 3
    assert fluka_beam.z_negative is False
    assert fluka_beam.beam_pos == (0, 0, -1.5)
    assert isclose(fluka_beam.beam_dir[0], 0.0, abs_tol=1e-16)
    assert isclose(fluka_beam.beam_dir[1], 0.0, abs_tol=1e-16)


def test_parse_fluka_beam_MeV_nucl(project_fluka_json):
    """Test if Fluka beam is parsed correctly"""
    beam_json = copy.deepcopy(project_fluka_json['beam'])
    beam_json['energyUnit'] = 'MeV/nucl'
    beam_json['energy'] = 100
    beam_json['particle']['id'] = 23
    beam_json['particle']['a'] = 3

    fluka_beam = parse_beam(beam_json)

    assert fluka_beam.energy_MeV == 300
    assert fluka_beam.particle_name == '3-HELIUM'


def test_parse_heavy_ions_MeV(project_fluka_json):
    """Test if Fluka beam is parsed correctly"""
    beam_json = copy.deepcopy(project_fluka_json['beam'])
    beam_json['energy'] = 300
    beam_json['energyUnit'] = 'MeV'
    beam_json['particle']['id'] = 25
    beam_json['particle']['a'] = 6
    beam_json['particle']['z'] = 12

    fluka_beam = parse_beam(beam_json)

    assert fluka_beam.energy_MeV == 50
    assert fluka_beam.particle_name == 'HEAVYION'
    assert fluka_beam.heavy_ion_a == 6
    assert fluka_beam.heavy_ion_z == 12


def test_parse_heavy_ions_MeV_nucl(project_fluka_json):
    """Test if Fluka beam is parsed correctly"""
    beam_json = copy.deepcopy(project_fluka_json['beam'])
    beam_json['energy'] = 300
    beam_json['energyUnit'] = 'MeV/nucl'
    beam_json['particle']['id'] = 25
    beam_json['particle']['a'] = 6
    beam_json['particle']['z'] = 12

    fluka_beam = parse_beam(beam_json)

    assert fluka_beam.energy_MeV == 300
    assert fluka_beam.particle_name == 'HEAVYION'
    assert fluka_beam.heavy_ion_a == 6
    assert fluka_beam.heavy_ion_z == 12
