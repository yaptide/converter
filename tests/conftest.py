from pathlib import Path
import pytest
import json

@pytest.fixture(scope='session')
def project_shieldhit_path() -> Path:
    """Path to SHIELD-HIT12A project.json file"""
    this_file_location = Path(__file__).parent
    json_file_path = this_file_location / 'shieldhit' / 'resources' / 'project.json'
    return json_file_path


@pytest.fixture(scope='session')
def project_shieldhit_json(project_shieldhit_path) -> dict:
    """Dictionary with project data for SHIELD-HIT12A"""
    with open(project_shieldhit_path, 'r') as file_handle:
        return json.load(file_handle)


@pytest.fixture(scope='session')
def project_shieldhit_with_sobp_dat_path() -> Path:
    """Path to SHIELD-HIT12A project.json file"""
    this_file_location = Path(__file__).parent
    json_file_path = this_file_location / 'shieldhit' / 'resources' / 'project_with_sobp.json'
    return json_file_path


@pytest.fixture(scope='session')
def project_shieldhit_json_with_sobp_dat(project_shieldhit_with_sobp_dat_path) -> dict:
    """Dictionary with project data for SHIELD-HIT12A"""
    with open(project_shieldhit_with_sobp_dat_path, 'r') as file_handle:
        return json.load(file_handle)
