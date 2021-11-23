import pytest
from os import path
from converter.shieldhit.parser import Parser
from converter.api import get_parser_from_str, run_parser
import json

_Beam_template = """
RNDSEED      	89736501     ! Random seed
JPART0       	2            ! Incident particle type
TMAX0      	{energy:3.6f}   0.0  ! Incident energy; (MeV/nucl)
NSTAT       {nstat:d}    -1 ! NSTAT, Step of saving
STRAGG          2            ! Straggling: 0-Off 1-Gauss, 2-Vavilov
MSCAT           2            ! Mult. scatt 0-Off 1-Gauss, 2-Moliere
NUCRE           0            ! Nucl.Reac. switcher: 1-ON, 0-OFF
"""


_Mat_template = """MEDIUM 1
ICRU 98
END
MEDIUM 2
ICRU 3
END
MEDIUM 3
ICRU 1
END
MEDIUM 4
ICRU 906
END
"""

_Detect_template = """Geometry Cyl
    Name ScoringCylinder
    R 0.0 10.0 1
    Z 0.0 30.0 400
Geometry Mesh
    Name MyMesh_YZ
    X -5.0  5.0    1
    Y -5.0  5.0    100
    Z  0.0  30.0   300
Output
    Filename mesh.bdo
    Geo ScoringCylinder
    Quantity Dose
    """

_Geo_template = """
    0    0          Unnamed geometry
  SPH    1       0.0       0.0       0.3       1.0
  SPH    2       0.3       0.0       0.0       1.0
  SPH    3       0.0       0.0      -0.3       1.0
  SPH    4      -0.3       0.0       0.0       1.0
  END
  001          +1     -2
  002          +3     +4     -2
  END
    1    2
    4    3
"""

_Test_dir = './test_runs'


@pytest.fixture
def output_dir(tmp_path_factory) -> str:
    """Fixture that creates a temporary dir for testing converter output."""
    output_dir = tmp_path_factory.mktemp(_Test_dir)
    return output_dir


@pytest.fixture
def parser() -> Parser:
    """Just a praser fixture."""
    return get_parser_from_str('shieldhit')


@pytest.fixture
def default_json() -> dict:
    """Creates default json."""
    with open(path.join(path.abspath("./input_examples"), 'example6.json'), 'r') as json_f:
        return json.load(json_f)


def test_if_beam_created(parser, default_json, output_dir) -> None:
    """Check if beam.dat file created"""
    run_parser(parser, default_json, output_dir)
    with open(path.join(output_dir, 'beam.dat')) as f:
        assert f.read() == _Beam_template.format(energy=150., nstat=1000)


def test_beam_energy(parser, default_json, output_dir) -> None:
    """Check if converter parsed energy"""
    energy = 312.
    default_json["beam"]["energy"] = energy
    run_parser(parser, default_json, output_dir)
    with open(path.join(output_dir, 'beam.dat')) as f:
        assert f.read() == _Beam_template.format(energy=energy, nstat=1000)


def test_if_mat_created(parser, default_json, output_dir) -> None:
    """Check if mat.dat file created"""
    run_parser(parser, default_json, output_dir)
    with open(path.join(output_dir, 'mat.dat')) as f:
        assert f.read() == _Mat_template


def test_if_detect_created(parser, default_json, output_dir) -> None:
    """Check if detect.dat file created"""
    run_parser(parser, default_json, output_dir)
    with open(path.join(output_dir, 'detect.dat')) as f:
        assert f.read() == _Detect_template


def test_if_geo_created(parser, default_json, output_dir) -> None:
    """Check if geo.dat file created"""
    run_parser(parser, default_json, output_dir)
    with open(path.join(output_dir, 'geo.dat')) as f:
        assert f.read() == _Geo_template
