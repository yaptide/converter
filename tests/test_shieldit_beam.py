import json
from pathlib import Path
from converter.api import get_parser_from_str, run_parser
from converter.common import Parser
import pytest


_Test_dir = './test_runs'

@pytest.fixture
def project_json() -> dict:
    """Fixture that provides a JSON with beam.dat dedicatet config."""
    this_script_path = Path(__file__).parent.absolute()
    with open(this_script_path / "resources" / "physics_settings.json", "r") as f:
        return json.load(f)
    return {}

@pytest.fixture
def output_dir(tmp_path_factory) -> Path:
    """Fixture that creates a temporary dir for testing converter output."""
    output_dir = tmp_path_factory.mktemp(_Test_dir)
    return Path(output_dir)


@pytest.fixture
def sh12a_parser() -> Parser:
    """Just a parser fixture."""
    return get_parser_from_str('shieldhit')


def test_project_json(project_json) -> None:
    """Check if project json is created correctly"""
    assert project_json
    assert "metadata" in project_json
    assert "project" in project_json
    assert "scene" in project_json
    assert "physic" in project_json
    assert "energyLoss" in project_json["physic"]
    assert "enableNuclearReactions" in project_json["physic"]
    assert "energyModelStraggling" in project_json["physic"]
    assert "multipleScattering" in project_json["physic"]


def test_parser(sh12a_parser) -> None:
    """Check if parser is created correctly"""
    assert sh12a_parser.info['version'] == 'unknown'
    assert sh12a_parser.info['simulator'] == 'shieldhit'

def test_generated_beam_dat(project_json, sh12a_parser, output_dir) -> None:
    """Check if beam.dat file created properly"""
    run_parser(sh12a_parser, project_json, output_dir)
    with open(output_dir / 'beam.dat') as f:
        input_text = f.read()
        assert input_text
        assert "STRAGG          1" in input_text
        assert "MSCAT           0" in input_text
        assert "NUCRE           0" in input_text