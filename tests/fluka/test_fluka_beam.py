from math import isclose
from converter.fluka.helper_parsers.beam_parser import BeamShape, parse_beam


def test_parse_fluka_beam(project_fluka_json):
    """Test if Fluka beam is parsed correctly"""

    beam_json = project_fluka_json["beam"]

    fluka_beam = parse_beam(beam_json)

    assert fluka_beam.energy == 0.07
    assert fluka_beam.particle_name == "PROTON"
    assert fluka_beam.shape == BeamShape.CIRCULAR
    assert fluka_beam.shape_x == 0
    assert fluka_beam.shape_y == 3
    assert fluka_beam.z_negative is False
    assert fluka_beam.beam_pos == (0, 0, -1.5)
    assert isclose(fluka_beam.beam_dir[0], 0.0, abs_tol=1e-16)
    assert isclose(fluka_beam.beam_dir[1], 0.0, abs_tol=1e-16)