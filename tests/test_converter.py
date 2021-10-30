import pytest
from converter.converter import BeamConfig, MatConfig, DetectConfig, GeoConfig


def test_default_beam_config_str() -> None:
    """Test if the default BeamConfig str representation is correct."""
    assert str(BeamConfig()) == """
RNDSEED      	89736501     ! Random seed
JPART0       	2            ! Incident particle type
TMAX0      	250.000000   0.0  ! Incident energy; (MeV/nucl)
NSTAT       10000    -1 ! NSTAT, Step of saving
STRAGG          2            ! Straggling: 0-Off 1-Gauss, 2-Vavilov
MSCAT           2            ! Mult. scatt 0-Off 1-Gauss, 2-Moliere
NUCRE           0            ! Nucl.Reac. switcher: 1-ON, 0-OFF
"""


def test_default_mat_config_str() -> None:
    """Test if the default MatConfig str representation is correct."""
    assert str(MatConfig()) == """MEDIUM 0
ICRU 276
END
"""


def test_default_detect_config_str() -> None:
    """Test if the default MatConfig str representation is correct."""
    assert str(DetectConfig()) == """Geometry Cyl
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


def test_default_geo_config_str() -> None:
    """Test if the default MatConfig str representation is correct."""
    assert str(GeoConfig()) == """
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
