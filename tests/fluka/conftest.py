import json
import pytest
from pathlib import Path

@pytest.fixture(scope='session')
def project_fluka_path() -> Path:
    """Path to SHIELD-HIT12A project.json file"""
    return Path(__file__).parent / 'project.json'

@pytest.fixture(scope='session')
def project_fluka_json(project_fluka_path) -> dict:
    """Dictionary with project data for SHIELD-HIT12A"""
    with open(project_fluka_path, 'r') as file_handle:
        return json.load(file_handle)

@pytest.fixture(scope='session')
def expected_output_path() -> Path:
    """Path to expected Fluka output"""
    return Path(__file__).parent / 'expected_fluka_output'