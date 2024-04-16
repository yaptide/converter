from converter.common import rotate, format_float
from scipy.spatial.transform import Rotation
import numpy as np
import pytest


@pytest.mark.parametrize('vector,angles,degrees', [([1, 0, 0], [90, 0, 0], True), ([0, 1, 0], [270, 0, 0], True),
                                                   ([1, 0, 0], [90, 90, 90], True), ([0, 0, 0], [45, 45, 45], True),
                                                   ([2, 3, 4], [30, 45, 60], True), ([1, 1, 1], [-45, -30, -60], True),
                                                   ([1, 1, 1], [270, 180, 360], True),
                                                   ([-1, -2, -3], [45, 45, 45], True), ([0, 1, 1], [45, 0, 0], True),
                                                   ([2, 4, -7], [23, -82, 213], True), ([1, 0, 0], [0, 0, 0], True),
                                                   ([0, 1, 0], [0, 0, 0], True), ([0, 0, 1], [0, 0, 0], True),
                                                   ([1, 0, 0], [np.pi / 2, 0, 0], False),
                                                   ([0, 1, 0], [np.pi / 2, 0, 0], False),
                                                   ([0, 0, 1], [np.pi / 2, 0, 0], False),
                                                   ([0, 1, 0], [0, np.pi / 2, 0], False),
                                                   ([0, 0, 1], [0, 0, np.pi / 2], False),
                                                   ([2, 4, -1], [np.pi / 4, np.pi / 3, np.pi / 2], False),
                                                   ([0, 0, 0], [45, 45, 45], True), ([0, 0, 1], [90, 0, 0], True),
                                                   ([0, 0, 1], [0, 0, 90], True), ([0, 0, 1], [0, 0, 180], True)])
def test_rotate(vector: list[float], angles: list[float], degrees: bool):
    """Test the rotate function with various inputs."""
    # Rotate using custom function
    result = rotate(vector, angles, degrees)

    # Rotate using SciPy
    r = Rotation.from_euler('xyz', angles, degrees=degrees)
    result_scipy = r.apply(vector)

    assert pytest.approx(result) == result_scipy
