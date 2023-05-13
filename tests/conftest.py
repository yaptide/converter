from pathlib import Path
import pytest
import json

@pytest.fixture(scope='session')
def project_shieldhit_json() -> dict:
    """Dictionary with project data for SHIELD-HIT12A"""
    this_file_location = Path(__file__).parent
    json_file_path = this_file_location / 'shieldhit' / 'resources' / 'project.json'
    with open(json_file_path, 'r') as file_handle:
        return json.load(file_handle)