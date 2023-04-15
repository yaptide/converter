import pytest
from os import path
from converter.shieldhit.parser import Parser
from converter.api import get_parser_from_str, run_parser

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

sv:Ph/Default/Modules = 1 "g4em-standard_opt0"
"""

_Test_dir = './test_runs'

@pytest.fixture
def parser() -> Parser:
    """Just a parser fixture."""
    return get_parser_from_str('topas')


@pytest.fixture
def output_dir(tmp_path_factory, parser) -> str:
    """Fixture that creates a temporary dir for testing converter output and runs the conversion there."""
    output_dir = tmp_path_factory.mktemp(_Test_dir)
    run_parser(parser, {}, output_dir)
    return output_dir


def test_if_beam_created(output_dir) -> None:
    """Check if topas_config.txt file created"""
    with open(path.join(output_dir, 'topas_config.txt')) as f:
        assert f.read() == _Config_str