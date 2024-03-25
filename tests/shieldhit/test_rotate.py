from converter.common import rotate
import pytest


@pytest.mark.parametrize(
    'vector,angles,expected',
    [
        ([1, 0, 0], [90, 0, 0], [1.0, 0.0, 0.0]),
        ([0, 1, 0], [270, 0, 0], [0.0, 0.0, -1.0]),
        # Add more test cases here
    ])
def test_rotate(vector, angles, expected):
    """Test the rotate function with various inputs."""
    result = rotate(vector, angles)
    assert result == expected, f'Expected {expected}, but got {result}'
