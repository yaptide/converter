from pathlib import Path
import pytest
import json

@pytest.fixture(scope='session')
def project_topas_json(project_shieldhit_json) -> dict:
    """We do not have yet project.json for TOPAS, so we use the one from SHIELD-HIT12A"""
    return project_shieldhit_json