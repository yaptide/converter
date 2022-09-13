import pytest
from os import path
from converter.shieldhit.parser import Parser
from converter.api import get_parser_from_str, run_parser

_Beam_str = """
RNDSEED      	89736501     ! Random seed
JPART0       	2            ! Incident particle type
TMAX0      	150.0  1.5       ! Incident energy; (MeV/nucl)
NSTAT       10000    0       ! NSTAT, Step of saving
STRAGG          2            ! Straggling: 0-Off 1-Gauss, 2-Vavilov
MSCAT           2            ! Mult. scatt 0-Off 1-Gauss, 2-Moliere
NUCRE           1            ! Nucl.Reac. switcher: 1-ON, 0-OFF
BEAMPOS 0 0 0 ! Position of the beam
BEAMDIR 0.0 0.0 ! Direction of the beam
BEAMSIGMA  -0.1 0.1  ! Beam extension
DELTAE   0.03   ! relative mean energy loss per transportation step
"""

_Mat_str = """MEDIUM 1
ICRU 276
END
"""

_Detect_str = """Geometry Cyl
    Name CylZ_Mesh
    R 0 10 1
    Z 0 20 400

Geometry Mesh
    Name YZ_Mesh
    X -0.5 0.5 1
    Y -2 2 80
    Z 0 20 400


Output
    Filename cylz.bdo
    Geo CylZ_Mesh
    Quantity DoseGy 

Output
    Filename yzmsh.bdo
    Geo YZ_Mesh
    Quantity DoseGy 
"""

_Geo_str = """
    0    0          Unnamed geometry
  RCC    1       0.0      10.0      10.0       0.0     -20.0       0.0
                10.0
  RCC    2       0.0      12.5       7.5       0.0     -25.0       0.0
                15.0
  RCC    3       0.0      15.0       5.0       0.0     -30.0       0.0
                20.0
  END
  001          +1
  002          +2     -1
  003          +3     -2
  END
    1    2    3
    1 1000    0
"""

_Test_dir = './test_runs'


@pytest.fixture
def parser() -> Parser:
    """Just a praser fixture."""
    return get_parser_from_str('sh_dummy')


@pytest.fixture
def output_dir(tmp_path_factory, parser) -> str:
    """Fixture that creates a temporary dir for testing converter output and runs the conversion there."""
    output_dir = tmp_path_factory.mktemp(_Test_dir)
    run_parser(parser, {}, output_dir)
    return output_dir


def test_if_beam_created(output_dir) -> None:
    """Check if beam.dat file created"""
    with open(path.join(output_dir, 'beam.dat')) as f:
        assert f.read() == _Beam_str


def test_if_mat_created(output_dir) -> None:
    """Check if mat.dat file created"""
    with open(path.join(output_dir, 'mat.dat')) as f:
        assert f.read() == _Mat_str


def test_if_detect_created(output_dir) -> None:
    """Check if detect.dat file created"""
    with open(path.join(output_dir, 'detect.dat')) as f:
        assert f.read() == _Detect_str


def test_if_geo_created(output_dir) -> None:
    """Check if geo.dat file created"""
    with open(path.join(output_dir, 'geo.dat')) as f:
        assert f.read() == _Geo_str
