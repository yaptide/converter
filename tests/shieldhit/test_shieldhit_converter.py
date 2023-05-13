import filecmp
import json
import logging
from pathlib import Path

import pytest

from converter.api import get_parser_from_str, run_parser
from converter.shieldhit.parser import Parser


def test_parser(sh12a_parser : Parser) -> None:
    """Check if parser is created correctly"""
    assert sh12a_parser
    assert sh12a_parser.info['version'] == ''
    assert sh12a_parser.info['simulator'] == 'shieldhit'

def test_project_json(project_shieldhit_json: dict) -> None:
    """Check if project json is created correctly"""
    assert project_shieldhit_json
    assert "metadata" in project_shieldhit_json
    assert "project" in project_shieldhit_json
    assert "scene" in project_shieldhit_json
    assert "physic" in project_shieldhit_json
    assert "energyLoss" in project_shieldhit_json["physic"]
    assert "enableNuclearReactions" in project_shieldhit_json["physic"]
    assert "energyModelStraggling" in project_shieldhit_json["physic"]
    assert "multipleScattering" in project_shieldhit_json["physic"]


@pytest.mark.parametrize('filename', ['beam.dat', 'mat.dat', 'detect.dat'])
def test_if_expected_files_created(sh12a_parser: Parser, project_shieldhit_json : dict, tmp_path : Path, path_to_dir_with_expected_output: Path, filename: str) -> None:
    """Check if all output files are created"""
    logging.info('Checking %s file', filename)
    run_parser(sh12a_parser, project_shieldhit_json, tmp_path)
    assert (tmp_path / filename).exists()
    assert (path_to_dir_with_expected_output / filename).exists()
    assert filecmp.cmp(tmp_path / filename, path_to_dir_with_expected_output / filename)

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
