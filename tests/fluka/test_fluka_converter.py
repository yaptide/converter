import pytest
from pathlib import Path
from converter.common import Parser
from converter.api import get_parser_from_str, run_parser
import logging
from difflib import Differ
from expected_fluka_output.fl_sim import expected_output

@pytest.fixture
def fluka_parser() -> Parser:
    """Parser fixture."""
    return get_parser_from_str("fluka")


def test_parser(fluka_parser: Parser) -> None:
    """Check if parser is created correctly."""
    assert fluka_parser.info["version"] == "unknown"
    assert fluka_parser.info["simulator"] == "fluka"
    assert fluka_parser.info["label"] == ""

@pytest.mark.parametrize('filename', ['fl_sim.inp'])
def test_if_inp_created(fluka_parser: Parser, project_fluka_json: dict, tmp_path: Path, filename: str) -> None:
    """Check if fl_sim.inp file created and equal to expected."""
    run_parser(fluka_parser, project_fluka_json, tmp_path)
    with open(tmp_path / filename) as generated_f:
        generated_content = generated_f.read()
        expected_equal_to_generated = generated_content == expected_output
        if not expected_equal_to_generated:
            logging.info("Generated file at %s", tmp_path / filename)
            differ = Differ()
            generated_f.seek(0)
            difference_lines = "\n".join(differ.compare([line.rstrip() for line in generated_f.readlines()],
                                                        [line.rstrip() for line in expected_output.splitlines()]))
            logging.info("Difference between files: %s", difference_lines)
        assert expected_equal_to_generated
