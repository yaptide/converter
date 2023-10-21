import pytest
from pathlib import Path
from converter.common import Parser
from converter.api import get_parser_from_str, run_parser
import filecmp
import logging
from difflib import Differ

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
def test_if_inp_created(fluka_parser: Parser, project_fluka_json: dict, tmp_path: Path,
                        expected_output_path: Path, filename: str) -> None:
    """Check if fl_sim.inp file created."""
    run_parser(fluka_parser, project_fluka_json, tmp_path)
    assert (expected_output_path / filename).exists()
    expected_equal_to_generated = filecmp.cmp(tmp_path / filename, expected_output_path / filename)
    if not expected_equal_to_generated:
        logging.info("Expected file at %s", expected_output_path / filename)
        logging.info("Generated file at %s", tmp_path / filename)
        with open(tmp_path / filename) as generated_f, open(expected_output_path / filename) as expected_f:
            differ = Differ()
            difference_lines = "\n".join(differ.compare(generated_f.readlines(), expected_f.readlines()))
            logging.info("Difference between files: %s", difference_lines)
    assert expected_equal_to_generated
