import pytest
from converter.shieldhit.parser import BeamConfig, MatConfig, DetectConfig
from converter.shieldhit.geo import GeoConfig

_Beam_template = """
RNDSEED      	89736501     ! Random seed
JPART0       	2            ! Incident particle type
TMAX0      	{energy:3.6f}   0.0  ! Incident energy; (MeV/nucl)
NSTAT       {nstat:d}    -1 ! NSTAT, Step of saving
STRAGG          2            ! Straggling: 0-Off 1-Gauss, 2-Vavilov
MSCAT           2            ! Mult. scatt 0-Off 1-Gauss, 2-Moliere
NUCRE           0            ! Nucl.Reac. switcher: 1-ON, 0-OFF
"""

_Beam_template_default = _Beam_template.format(energy=150, nstat=1000)

_Mat_template_default = """MEDIUM 0
ICRU 276
END
"""

_Detect_template_default = """Geometry Cyl
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

_Geo_template_default = """
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


def test_default_beam_config_str() -> None:
    """Test if the default BeamConfig str representation is correct."""
    assert str(BeamConfig()) == _Beam_template_default


def test_default_mat_config_str() -> None:
    """Test if the default MatConfig str representation is correct."""
    assert str(MatConfig()) == _Mat_template_default


def test_default_detect_config_str() -> None:
    """Test if the default MatConfig str representation is correct."""
    assert str(DetectConfig()) == _Detect_template_default


def test_default_geo_config_str() -> None:
    """Test if the default MatConfig str representation is correct."""
    assert str(GeoConfig()) == _Geo_template_default
