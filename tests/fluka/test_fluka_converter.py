import pytest
import json
from pathlib import Path
from converter.common import Parser
from converter.api import get_parser_from_str, run_parser

_expected_fluka_input_content = """TITLE
proton beam simulation
* default physics settings for hadron therapy
DEFAULTS                                                              HADROTHE
* beam source
BEAM      1.5000E-01                                                  PROTON
* beam source position
BEAMPOS          0.0       0.0    -100.0
* geometry description starts here
GEOBEGIN                                                              COMBNAME
    0    0
* black body sphere
SPH blkbody    0.0 0.0 0.0 10000.0
* air shpere
SPH air        0.0 0.0 0.0 100.0
* target cylinder
RCC target     0.0 0.0 0.0 0.0 0.0 10.0 5.0
END
* outer black body region
Z_BBODY      5 +blkbody -air
* inner air region
Z_AIR        5 +air -target
* target region
Z_TARGET     5 +target
END
GEOEND
ASSIGNMA    BLCKHOLE   Z_BBODY
ASSIGNMA         AIR     Z_AIR
ASSIGNMA       WATER  Z_TARGET
* scoring NEUTRON on mesh z
USRBIN           0.0   NEUTRON       -21       0.5       0.5       5.0n_z
USRBIN          -0.5      -0.5       0.0         1         1       500&
* scoring NEUTRON on mesh yz
USRBIN           0.0   NEUTRON       -22       0.1       5.0       5.0n_yz
USRBIN          -0.1      -5.0       0.0         1       500       500&
* scoring NEUTRON on mesh xy
USRBIN           0.0   NEUTRON       -23       5.0       5.0       2.9n_xy
USRBIN          -5.0      -5.0       2.8       500       500         1&
* scoring NEUTRON on mesh zx
USRBIN           0.0   NEUTRON       -24       5.0       0.1       5.0n_zx
USRBIN          -5.0      -0.1       0.0       500         1       500&
* scoring ENERGY on mesh z
USRBIN           0.0    ENERGY       -25       0.5       0.5       5.0en_z
USRBIN          -0.5      -0.5       0.0         1         1       500&
* scoring ENERGY on mesh yz
USRBIN           0.0    ENERGY       -26       0.1       5.0       5.0en_yz
USRBIN          -0.1      -5.0       0.0         1       500       500&
* scoring ENERGY on mesh xy
USRBIN           0.0    ENERGY       -27       5.0       5.0       2.9en_xy
USRBIN          -5.0      -5.0       2.8       500       500         1&
* scoring ENERGY on mesh zx
USRBIN           0.0    ENERGY       -28       5.0       0.1       5.0en_zx
USRBIN          -5.0      -0.1       0.0       500         1       500&
* random number generator settings
RANDOMIZ                   137
* number of particles to simulate
START          10000
STOP
"""

@pytest.fixture
def parser() -> Parser:
    """Parser fixture."""
    return get_parser_from_str("fluka")

@pytest.fixture
def default_json() -> dict:
    """Creates default json."""
    file_path = Path(__file__).resolve().parent / 'resources' / 'project.json'
    with open(file_path, 'r') as json_f:
        return json.load(json_f)


def test_parser(parser: Parser) -> None:
    """Check if parser is created correctly."""
    assert parser.info["version"] == "unknown"
    assert parser.info["simulator"] == "fluka"
    assert parser.info["label"] == ""

def test_if_inp_created(parser: Parser, default_json: dict, tmp_path: Path) -> None:
    """Check if fl_sim.inp file created."""
    run_parser(parser, default_json, tmp_path)
    with open(tmp_path / "fl_sim.inp") as f:
        assert f.read() == _expected_fluka_input_content
