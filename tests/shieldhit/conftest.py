from pathlib import Path
import pytest
import json

@pytest.fixture(scope='session')
def default_json() -> dict:
    """Creates default json."""
    example_json = Path(__file__).parent.parent / 'input_examples' / 'sh_parser_test.json'
    with open(example_json, 'r') as json_f:
        return json.load(json_f)