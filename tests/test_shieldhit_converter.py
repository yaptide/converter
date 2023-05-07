import filecmp
import json
import logging
from os import path
from pathlib import Path

import pytest

from converter.api import get_parser_from_str, run_parser
from converter.shieldhit.parser import Parser


@pytest.fixture
def parser() -> Parser:
    """Just a praser fixture."""
    return get_parser_from_str('shieldhit')


@pytest.fixture
def default_json() -> dict:
    """Creates default json."""
    example_json = Path(__file__).parent.parent / 'input_examples' / 'sh_parser_test.json'
    with open(example_json, 'r') as json_f:
        return json.load(json_f)

@pytest.mark.parametrize('filename', ['beam.dat', 'mat.dat', 'detect.dat', 'geo.dat'])
def test_if_expected_files_created(parser: Parser, default_json : dict, tmp_path : Path, filename: str) -> None:
    """Check if all output files are created"""
    logging.info('Checking %s file', filename)
    run_parser(parser, default_json, tmp_path)
    dir_with_expected_files = Path(__file__).parent.parent / 'input_examples' / 'expected_shieldhit_output'
    assert (tmp_path / filename).exists() == True
    assert (dir_with_expected_files / filename).exists() == True
    assert filecmp.cmp(tmp_path / filename, dir_with_expected_files / filename) == True

@pytest.mark.parametrize('filename', ['geo.dat'])
@pytest.mark.skip(reason="Something is wrong with geo.dat file.")
def test_if_expected_files_created(parser: Parser, default_json : dict, tmp_path : Path, filename: str) -> None:
    """Check if all output files are created"""
    logging.info('Checking %s file', filename)
    run_parser(parser, default_json, tmp_path)
    dir_with_expected_files = Path(__file__).parent.parent / 'input_examples' / 'expected_shieldhit_output'
    assert (tmp_path / filename).exists() == True
    assert (dir_with_expected_files / filename).exists() == True
    assert filecmp.cmp(tmp_path / filename, dir_with_expected_files / filename) == True