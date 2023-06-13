from typing import Optional
import pytest

from converter.shieldhit.geo import GeoMatConfig
from converter.shieldhit.parser import BeamConfig, DetectConfig

_Beam_template = """
RNDSEED      	89736501     ! Random seed
JPART0       	2            ! Incident particle type
TMAX0      	{energy} {energy_spread}       ! Incident energy and energy spread; both in (MeV/nucl)
! no energy cutoffs
NSTAT       {nstat:d}    0       ! NSTAT, Step of saving
STRAGG          2            ! Straggling: 0-Off 1-Gauss, 2-Vavilov
MSCAT           2            ! Mult. scatt 0-Off 1-Gauss, 2-Moliere
NUCRE           1            ! Nucl.Reac. switcher: 1-ON, 0-OFF
! no beam modulator
BEAMPOS 0 0 0 ! Position of the beam
BEAMDIR 0.0 0.0 ! Direction of the beam
BEAMSIGMA  -0.1 0.1  ! Beam extension
! no BEAMSAD value
DELTAE   0.03   ! relative mean energy loss per transportation step
"""

_Beam_template_default = _Beam_template.format(energy=150., energy_spread=1.5, nstat=10000)

_Mat_template_default = """MEDIUM 1
ICRU 276
END
"""

_Detect_template_default = """Geometry Cyl
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

_Geo_template_default = """
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


def test_energy_cutoff() -> None:
    """Test if the energy cutoffs are correctly set."""
    beam = BeamConfig()
    beam.energy_low_cutoff = 0.0
    beam.energy_high_cutoff = 10.0
    assert "TCUT0 0.0 10.0  ! energy cutoffs [MeV]" in str(beam)

    beam.energy_low_cutoff = None
    assert "TCUT0" not in str(beam)

    beam.energy_high_cutoff = None
    assert "TCUT0" not in str(beam)


@pytest.mark.parametrize('sad_x, sad_y', [
    (None, None),
    (200, None),
    (210, 250),
])
def test_sad_parameter(sad_x: Optional[float], sad_y: Optional[float]) -> None:
    """Test if the BEAMSAD values are correctly set."""
    beam = BeamConfig()
    beam.sad_x = sad_x
    beam.sad_y = sad_y
    if sad_x is None and sad_y is None:
        assert "! no BEAMSAD value" in str(beam)
    elif sad_x is not None and sad_y is None:
        assert f"BEAMSAD {sad_x}   ! BEAMSAD value [cm]" in str(beam)
    elif sad_x is not None and sad_y is not None:
        assert f"BEAMSAD {sad_x} {sad_y}  ! BEAMSAD value [cm]" in str(beam)
