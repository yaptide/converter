from pathlib import Path
import pytest
from converter.api import get_parser_from_str

from converter.common import Parser


@pytest.fixture(scope='session')
def sh12a_parser() -> Parser:
    """Just a parser fixture."""
    return get_parser_from_str('shieldhit')


@pytest.fixture(scope='session')
def path_to_dir_with_expected_output(project_shieldhit_path: Path) -> Path:
    """Just a parser fixture."""
    return project_shieldhit_path.parent / 'expected_shieldhit_output'


@pytest.fixture(scope='session')
def path_to_dir_with_expected_output_with_sobp_dat(project_shieldhit_with_sobp_dat_path: Path) -> Path:
    """Just a parser fixture."""
    return project_shieldhit_with_sobp_dat_path.parent / 'expected_shieldhit_output_with_sobp_dat'
