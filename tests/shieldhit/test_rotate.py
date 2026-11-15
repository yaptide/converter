from converter.common import rotate
from scipy.spatial.transform import Rotation
import math
import pytest


@pytest.mark.parametrize(
    "vector,angles,degrees",
    [
        ([1, 0, 0], [90, 0, 0], True),
        ([0, 1, 0], [270, 0, 0], True),
        ([1, 0, 0], [90, 90, 90], True),
        ([0, 0, 0], [45, 45, 45], True),
        ([2, 3, 4], [30, 45, 60], True),
        ([1, 1, 1], [-45, -30, -60], True),
        ([1, 1, 1], [270, 180, 360], True),
        ([-1, -2, -3], [45, 45, 45], True),
        ([0, 1, 1], [45, 0, 0], True),
        ([2, 4, -7], [23, -82, 213], True),
        ([1, 0, 0], [0, 0, 0], True),
        ([0, 1, 0], [0, 0, 0], True),
        ([0, 0, 1], [0, 0, 0], True),
        ([1, 0, 0], [math.pi / 2, 0, 0], False),
        ([0, 1, 0], [math.pi / 2, 0, 0], False),
        ([0, 0, 1], [math.pi / 2, 0, 0], False),
        ([0, 1, 0], [0, math.pi / 2, 0], False),
        ([0, 0, 1], [0, 0, math.pi / 2], False),
        ([2, 4, -1], [math.pi / 4, math.pi / 3, math.pi / 2], False),
        ([0, 0, 0], [45, 45, 45], True),
        ([0, 0, 1], [90, 0, 0], True),
        ([0, 0, 1], [0, 0, 90], True),
        ([0, 0, 1], [0, 0, 180], True),
    ],
)
def test_rotate(vector: list[float], angles: list[float], degrees: bool):
    """Test the rotate function with various inputs."""
    # Rotate using custom function
    result = rotate(vector, angles, degrees)

    # Rotate using SciPy
    r = Rotation.from_euler("XYZ", angles, degrees=degrees)
    result_scipy = r.apply(vector)

    assert pytest.approx(result) == result_scipy


@pytest.mark.parametrize(
    "vector,angles,expected",
    [
        # expected values computed with three.js (Euler 'XYZ'), as the editor rotates figures
        ([0, 0, 1], [30, 40, 50], [0.6428, -0.3830, 0.6634]),
        ([0.3, -1.2, 2.5], [30, 40, 50], [2.4589, -1.0691, 0.7687]),
    ],
)
def test_rotate_matches_editor(vector: list[float], angles: list[float], expected: list[float]):
    """The converter must orient figures the same way as the editor (three.js)."""
    assert rotate(vector, angles) == pytest.approx(expected, abs=1e-4)
