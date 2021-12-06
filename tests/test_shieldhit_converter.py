import pytest
from os import path
from converter.shieldhit.parser import Parser
from converter.api import get_parser_from_str, run_parser
import json

_Beam_template = """
RNDSEED      	89736501     ! Random seed
JPART0       	2            ! Incident particle type
TMAX0      	{energy:3.1f}  1.5       ! Incident energy; (MeV/nucl)
NSTAT       {nstat:d}    0       ! NSTAT, Step of saving
STRAGG          2            ! Straggling: 0-Off 1-Gauss, 2-Vavilov
MSCAT           2            ! Mult. scatt 0-Off 1-Gauss, 2-Moliere
NUCRE           1            ! Nucl.Reac. switcher: 1-ON, 0-OFF
"""


_Mat_template = """MEDIUM 1
ICRU 170
END
"""

_Detect_template = """Geometry Cyl
    Name CylZ_Mesh
    R  0.0  10.0    1
    Z  0.0  20.0    400

Geometry Mesh
    Name YZ_Mesh
    X -0.5  0.5    1
    Y -2.0  2.0    80
    Z  0.0  20.0   400


Output
    Filename cylz.bdo
    Geo CylZ_Mesh
    Quantity DoseGy

Output
    Filename yzmsh.bdo
    Geo YZ_Mesh
    Quantity DoseGy
    """

_Geo_template = """
    0    0          Unnamed geometry
  BOX    1      -0.50.22757704      -0.5       1.0       0.0       0.0
                 0.0       1.0       0.0       0.0       0.0       1.0
  BOX    2      -0.5-0.2244695      -0.5       1.0       0.0       0.0
                 0.0       1.0       0.0       0.0       0.0       1.0
  SPH    3       0.0       0.0       0.0       1.0
  BOX    4      -1.5      -1.5      -1.5       3.0       0.0       0.0
                 0.0       3.0       0.0       0.0       0.0       3.0
  BOX    5      -2.5      -2.5      -2.5       5.0       0.0       0.0
                 0.0       5.0       0.0       0.0       0.0       5.0
  END
  001          +1     +3OR   +2
  002          +4     -1     -2OR   +4     -3     -2
  003          -4     +5
  END
    1    2    3
    1 1000    0
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
    with open(path.join(path.abspath("./input_examples"), 'sh_parser_test.json'), 'r') as json_f:
        return json.load(json_f)


def test_if_beam_created(parser, default_json, output_dir) -> None:
    """Check if beam.dat file created"""
    run_parser(parser, default_json, output_dir)
    with open(path.join(output_dir, 'beam.dat')) as f:
        assert f.read() == _Beam_template.format(energy=150., nstat=10000)


def test_beam_energy(parser, default_json, output_dir) -> None:
    """Check if converter parsed energy"""
    energy = 312.
    default_json["beam"]["energy"] = energy
    run_parser(parser, default_json, output_dir)
    with open(path.join(output_dir, 'beam.dat')) as f:
        assert f.read() == _Beam_template.format(energy=energy, nstat=10000)


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
