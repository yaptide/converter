import pytest
from pathlib import Path

@pytest.fixture(scope='session')
def project_fluka_json(project_shieldhit_json) -> dict:
    """We do not have yet project.json for FLUKA, so we use the one from SHIELD-HIT12A"""
    return project_shieldhit_json

@pytest.fixture(scope='session')
def expected_output_path() -> Path:
    """Just a parser fixture."""
    return Path(__file__).parent / 'expected_fluka_output'