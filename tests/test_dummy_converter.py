import pytest
import tempfile
from os import path
from converter.converter import BeamConfig, MatConfig, DetectConfig, GeoConfig, DummmyParser, Runner

BEAM_STR = """
RNDSEED      	89736501     ! Random seed
JPART0       	2            ! Incident particle type
TMAX0      	250.000000   0.0  ! Incident energy; (MeV/nucl)
NSTAT       10000    -1 ! NSTAT, Step of saving
STRAGG          2            ! Straggling: 0-Off 1-Gauss, 2-Vavilov
MSCAT           2            ! Mult. scatt 0-Off 1-Gauss, 2-Moliere
NUCRE           0            ! Nucl.Reac. switcher: 1-ON, 0-OFF
"""
MAT_STR = """MEDIUM 0
ICRU 276
END
"""

DETECT_STR = """Geometry Cyl
    Name ScoringCylinder
    R 0.0 10.0 10
    Z 0.0 30.0 10
Geometry Mesh
    Name MyMesh_YZ
    X -5.0  5.0    10
    Y -5.0  5.0    10
    Z  0.0  30.0   10
Output
    Filename mesh.bdo
    Geo ScoringCylinder
    Quantity Dose
    """

GEO_STR = """
*---><---><--------><------------------------------------------------>
    0    0           protons, H2O 30 cm cylinder, r=10, 1 zone
*---><---><--------><--------><--------><--------><--------><-------->
  RCC    1       0.0       0.0       0.0       0.0       0.0      30.0
                10.0
  RCC    2       0.0       0.0      -5.0       0.0       0.0      35.0
                15.0
  RCC    3       0.0       0.0     -10.0       0.0       0.0      40.0
                20.0
  END
  001          +1
  002          +2     -1
  003          +3     -2
  END
* material codes: 1 - liquid water (ICRU material no 276), 1000 - vacuum, 0 - black body
    1    2    3
    1 1000    0
"""

TEST_DIR = tempfile.TemporaryDirectory()


def test_default_beam_config_str() -> None:
    """Test if the default BeamConfig str representation is correct."""
    assert str(BeamConfig()) == BEAM_STR


def test_default_mat_config_str() -> None:
    """Test if the default MatConfig str representation is correct."""
    assert str(MatConfig()) == MAT_STR


def test_default_detect_config_str() -> None:
    """Test if the default MatConfig str representation is correct."""
    assert str(DetectConfig()) == DETECT_STR


def test_default_geo_config_str() -> None:
    """Test if the default MatConfig str representation is correct."""
    assert str(GeoConfig()) == GEO_STR


def test_parser_run() -> None:
    """Test if dummy parser generates output files corectly"""
    dummy_runner = Runner(DummmyParser(), {}, TEST_DIR.name)
    dummy_runner.run_parser()


def test_if_beam_created() -> None:
    """Check if beam.dat file created"""
    with open(path.join(TEST_DIR.name, 'beam.dat')) as f:
        assert f.read() == BEAM_STR


def test_if_mat_created() -> None:
    """Check if mat.dat file created"""
    with open(path.join(TEST_DIR.name, 'mat.dat')) as f:
        assert f.read() == MAT_STR


def test_if_detect_created() -> None:
    """Check if detect.dat file created"""
    with open(path.join(TEST_DIR.name, 'detect.dat')) as f:
        assert f.read() == DETECT_STR


def test_if_geo_created() -> None:
    """Check if geo.dat file created"""
    with open(path.join(TEST_DIR.name, 'geo.dat')) as f:
        assert f.read() == GEO_STR
