import filecmp
import json
import logging
from pathlib import Path

import pytest

from converter.api import get_parser_from_str, run_parser
from converter.shieldhit.parser import Parser


@pytest.fixture
def parser() -> Parser:
    """SHIELD-HIT12A parser fixture"""
    return get_parser_from_str('shieldhit')




def test_if_parser_created(parser: Parser) -> None:
    """Check if parser is created"""
    assert parser
    assert parser.info['version'] == ''
    assert parser.info['label'] == ''
    assert parser.info['simulator'] == 'shieldhit'

@pytest.mark.parametrize('filename', ['beam.dat', 'mat.dat', 'detect.dat'])
def test_if_expected_files_created(parser: Parser, default_json : dict, tmp_path : Path, filename: str) -> None:
    """Check if all output files are created"""
    logging.info('Checking %s file', filename)
    run_parser(parser, default_json, tmp_path)
    dir_with_expected_files = Path(__file__).parent.parent / 'input_examples' / 'expected_shieldhit_output'
    assert (tmp_path / filename).exists()
    assert (dir_with_expected_files / filename).exists()
    assert filecmp.cmp(tmp_path / filename, dir_with_expected_files / filename)

@pytest.mark.parametrize('filename', ['geo.dat'])
@pytest.mark.skip(reason="Something is wrong with geo.dat file.")
def test_to_be_fixed(parser: Parser, default_json : dict, tmp_path : Path, filename: str) -> None:
    """Check if all output files are created"""
    logging.info('Checking %s file', filename)
    run_parser(parser, default_json, tmp_path)
    dir_with_expected_files = Path(__file__).parent.parent / 'input_examples' / 'expected_shieldhit_output'
    assert (tmp_path / filename).exists()
    assert (dir_with_expected_files / filename).exists()
    assert filecmp.cmp(tmp_path / filename, dir_with_expected_files / filename)
