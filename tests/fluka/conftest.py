import json
import pytest
from pathlib import Path


@pytest.fixture(scope='session')
def project_fluka_path() -> Path:
    """Path to SHIELD-HIT12A project.json file"""
    return Path(__file__).parent / 'project.json'


@pytest.fixture(scope='session')
def project_fluka_json(project_fluka_path) -> dict:
    """Dictionary with project data for Fluka"""
    with open(project_fluka_path, 'r') as file_handle:
        return json.load(file_handle)


@pytest.fixture(scope='session')
def project2_fluka_path() -> Path:
    """Path to SHIELD-HIT12A project.json file"""
    return Path(__file__).parent / 'project2.json'


@pytest.fixture(scope='session')
def project2_fluka_json(project2_fluka_path) -> dict:
    """Dictionary with project data for Fluka"""
    with open(project2_fluka_path, 'r') as file_handle:
        return json.load(file_handle)


@pytest.fixture(scope='session')
def project3_fluka_path() -> Path:
    """Path to SHIELD-HIT12A project.json file"""
    return Path(__file__).parent / 'project3.json'


@pytest.fixture(scope='session')
def project3_fluka_json(project3_fluka_path) -> dict:
    """Dictionary with project data for Fluka"""
    with open(project3_fluka_path, 'r') as file_handle:
        return json.load(file_handle)


@pytest.fixture(scope='session')
def project4_fluka_path() -> Path:
    """Path to Fluka project.json file"""
    return Path(__file__).parent / 'project4.json'


@pytest.fixture(scope='session')
def project4_fluka_json(project4_fluka_path) -> dict:
    """Dictionary with project data for Fluka"""
    with open(project4_fluka_path, 'r') as file_handle:
        return json.load(file_handle)
