import pytest
from pathlib import Path
from converter.api import get_parser_from_str, run_parser
from converter.common import Parser
import json

_Config_str = """s:Ge/MyBox/Type     = "TsBox"
s:Ge/MyBox/Material = "Air"
s:Ge/MyBox/Parent   = "World"
d:Ge/MyBox/HLX      = 2.5 m
d:Ge/MyBox/HLY      = 2. m
d:Ge/MyBox/HLZ      = 1. m
d:Ge/MyBox/TransX   = 2. m
d:Ge/MyBox/TransY   = 0. m
d:Ge/MyBox/TransZ   = 0. m
d:Ge/MyBox/RotX     = 0. deg
d:Ge/MyBox/RotY     = 0. deg
d:Ge/MyBox/RotZ     = 0. deg

s:So/Demo/Type = "Beam"
s:So/Demo/Component = "BeamPosition"
s:So/Demo/BeamParticle = "proton"
d:So/Demo/BeamEnergy = 1694.23 MeV
u:So/Demo/BeamEnergySpread = 0.757504
s:So/Demo/BeamPositionDistribution = "Gaussian"
s:So/Demo/BeamPositionCutoffShape = "Ellipse"
d:So/Demo/BeamPositionCutoffX = 10. cm
d:So/Demo/BeamPositionCutoffY = 10. cm
d:So/Demo/BeamPositionSpreadX = 0.65 cm
d:So/Demo/BeamPositionSpreadY = 0.65 cm
s:So/Demo/BeamAngularDistribution = "Gaussian"
d:So/Demo/BeamAngularCutoffX = 90. deg
d:So/Demo/BeamAngularCutoffY = 90. deg
d:So/Demo/BeamAngularSpreadX = 0.0032 rad
d:So/Demo/BeamAngularSpreadY = 0.0032 rad
i:So/Demo/NumberOfHistoriesInRun = 10000
i:Ts/ShowHistoryCountAtInterval = 100

s:Ge/BeamPosition/Parent="World"
s:Ge/BeamPosition/Type="Group"
d:Ge/BeamPosition/TransX=0. m
d:Ge/BeamPosition/TransY=0. m
d:Ge/BeamPosition/TransZ= Ge/World/HLZ m
d:Ge/BeamPosition/RotX=180. deg
d:Ge/BeamPosition/RotY=0. deg
d:Ge/BeamPosition/RotZ=0. deg

s:Sc/Dose/Quantity                  = "DoseToWater"
s:Sc/Dose/Component                 = "WaterPhantom"
s:Sc/Dose/IfOutputFileAlreadyExists = "Overwrite"
s:Sc/Dose/OutputType                = "CSV"

s:Ge/WaterPhantom/Parent            = "MyBox"
s:Ge/WaterPhantom/Type              = "TsBox"
s:Ge/WaterPhantom/Material          = "G4_WATER"
d:Ge/WaterPhantom/HLX               = 2.5 m
d:Ge/WaterPhantom/HLY               = 2. m
d:Ge/WaterPhantom/HLZ               = 0.1 cm
i:Ge/WaterPhantom/XBins             = 80
i:Ge/WaterPhantom/YBins             = 80
i:Ge/WaterPhantom/ZBins             = 1
d:Ge/WaterPhantom/TransZ            = 0. cm
s:Ge/WaterPhantom/DrawingStyle      = "Solid"
s:Ge/WaterPhantom/Color             = "skyblue"

sv:Ph/Default/Modules = 1 "g4em-standard_opt0"
"""

_Test_dir = './test_runs'

@pytest.fixture
def parser() -> Parser:
    """Just a parser fixture."""
    return get_parser_from_str('topas')

@pytest.fixture
def default_json() -> dict:
    """Creates default json."""
    file_path = Path.cwd() / "input_examples" / "topas_parser_test.json"
    with file_path.open(mode='r') as json_f:
        return json.load(json_f)

@pytest.fixture
def output_dir(tmp_path_factory, parser, default_json) -> str:
    """Fixture that creates a temporary dir for testing converter output and runs the conversion there."""
    output_dir = tmp_path_factory.mktemp(_Test_dir)
    run_parser(parser, default_json, output_dir)
    return output_dir


def test_if_config_created(output_dir) -> None:
    """Check if topas_config.txt file created"""
    output_file = output_dir.joinpath('topas_config.txt')
    with output_file.open(mode='r') as f:
        assert f.read() == _Config_str