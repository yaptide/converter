from difflib import Differ
import filecmp
import logging
from pathlib import Path

import pytest

from converter.api import run_parser
from converter.shieldhit.parser import Parser


def test_parser(sh12a_parser: Parser) -> None:
    """Check if parser is created correctly"""
    assert sh12a_parser
    assert sh12a_parser.info['version'] == ''
    assert sh12a_parser.info['simulator'] == 'shieldhit'
    assert sh12a_parser.info['label'] == ''


def test_project_json(project_shieldhit_json: dict) -> None:
    """Check if project json is created correctly"""
    assert project_shieldhit_json
    assert "metadata" in project_shieldhit_json
    assert "project" in project_shieldhit_json
    assert "figureManager" in project_shieldhit_json
    assert "physic" in project_shieldhit_json
    assert "energyLoss" in project_shieldhit_json["physic"]
    assert "enableNuclearReactions" in project_shieldhit_json["physic"]
    assert "energyModelStraggling" in project_shieldhit_json["physic"]
    assert "multipleScattering" in project_shieldhit_json["physic"]


@pytest.mark.parametrize('filename', ['beam.dat', 'mat.dat', 'detect.dat'])
def test_if_expected_files_created(sh12a_parser: Parser, project_shieldhit_json: dict, tmp_path: Path,
                                   path_to_dir_with_expected_output: Path, filename: str) -> None:
    """Check if all output files are created"""
    logging.info('Checking %s file', filename)
    run_parser(sh12a_parser, project_shieldhit_json, tmp_path)
    assert (tmp_path / filename).exists()
    assert (path_to_dir_with_expected_output / filename).exists()
    expected_equal_to_generated = filecmp.cmp(tmp_path / filename, path_to_dir_with_expected_output / filename)
    if not expected_equal_to_generated:
        logging.info("Expected file at %s", path_to_dir_with_expected_output / filename)
        logging.info("Generated file at %s", tmp_path / filename)
        logging.info("Difference between files:")
        with open(tmp_path / filename) as generated_f, open(path_to_dir_with_expected_output / filename) as expected_f:
            differ = Differ()
            difference_lines = "\n".join(differ.compare(generated_f.readlines(), expected_f.readlines()))
            logging.info("Difference between files: %s", difference_lines)
    assert expected_equal_to_generated


@pytest.mark.parametrize('filename', ['beam.dat', 'mat.dat', 'detect.dat', 'sobp.dat'])
def test_if_expected_files_created_with_sobp_dat(sh12a_parser: Parser, project_shieldhit_json_with_sobp_dat: dict,
                                                 tmp_path: Path, path_to_dir_with_expected_output_with_sobp_dat: Path,
                                                 filename: str) -> None:
    """Check if all output files are created"""
    logging.info('Checking %s file', filename)
    run_parser(sh12a_parser, project_shieldhit_json_with_sobp_dat, tmp_path)
    assert (tmp_path / filename).exists()
    assert (path_to_dir_with_expected_output_with_sobp_dat / filename).exists()
    expected_equal_to_generated = filecmp.cmp(
        tmp_path / filename, path_to_dir_with_expected_output_with_sobp_dat / filename)
    if not expected_equal_to_generated:
        logging.info("Expected file at %s", path_to_dir_with_expected_output_with_sobp_dat / filename)
        logging.info("Generated file at %s", tmp_path / filename)
        logging.info("Difference between files:")
        expected_file_path = path_to_dir_with_expected_output_with_sobp_dat / filename
        with open(tmp_path / filename) as generated_f, open(expected_file_path) as expected_f:
            differ = Differ()
            difference_lines = "\n".join(differ.compare(generated_f.readlines(), expected_f.readlines()))
            logging.info("Difference between files: %s", difference_lines)
    assert expected_equal_to_generated


@pytest.mark.parametrize('filename', ['geo.dat'])
@pytest.mark.skip(reason="Something is wrong with geo.dat file.")
def test_to_be_fixed(parser: Parser, default_json: dict, tmp_path: Path, filename: str) -> None:
    """Check if all output files are created"""
    logging.info('Checking %s file', filename)
    run_parser(parser, default_json, tmp_path)
    dir_with_expected_files = Path(__file__).parent.parent / 'input_examples' / 'expected_shieldhit_output'
    assert (tmp_path / filename).exists()
    assert (dir_with_expected_files / filename).exists()
    expected_equal_to_generated = filecmp.cmp(tmp_path / filename, dir_with_expected_files / filename)
    if not expected_equal_to_generated:
        logging.info("Expected file at %s", tmp_path / filename)
    assert filecmp.cmp(tmp_path / filename, dir_with_expected_files / filename)
