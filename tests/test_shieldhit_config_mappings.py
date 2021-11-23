import pytest
from converter.shieldhit.parser import BeamConfig, DetectConfig
from converter.shieldhit.geo import GeoMatConfig

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

_Mat_template_default = """MEDIUM 1
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
    0    0          Unnamed geometry
  SPH    1       0.0       0.0       0.0       1.0
  END
  001          +1
  END
    1
    0
"""


def test_default_beam_config_str() -> None:
    """Test if the default BeamConfig str representation is correct."""
    assert str(BeamConfig()) == _Beam_template_default


def test_default_mat_config_str() -> None:
    """Test if the default MatConfig str representation is correct."""
    assert GeoMatConfig().get_mat_string() == _Mat_template_default


def test_default_detect_config_str() -> None:
    """Test if the default MatConfig str representation is correct."""
    assert str(DetectConfig()) == _Detect_template_default


def test_default_geo_config_str() -> None:
    """Test if the default MatConfig str representation is correct."""
    assert GeoMatConfig().get_geo_string() == _Geo_template_default
