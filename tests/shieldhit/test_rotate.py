from converter.common import rotate, format_float
from scipy.spatial.transform import Rotation
import pytest


@pytest.mark.parametrize('vector,angles', [([1, 0, 0], [90, 0, 0]), ([0, 1, 0], [270, 0, 0]), ([1, 0, 0], [90, 90, 90]),
                                           ([0, 0, 0], [45, 45, 45]), ([2, 3, 4], [30, 45, 60]),
                                           ([1, 1, 1], [-45, -30, -60]), ([1, 1, 1], [270, 180, 360]),
                                           ([-1, -2, -3], [45, 45, 45]), ([0, 1, 1], [45, 0, 0]),
                                           ([2, 4, -7], [23, -82, 213])])
def test_rotate(vector: list[float], angles: list[float]):
    """Test the rotate function with various inputs. Expects angles as degrees"""
    # Rotate using custom function
    result = rotate(vector, angles)

    # Rotate using SciPy
    r = Rotation.from_euler('xyz', angles, degrees=True)
    result_scipy = r.apply(vector)

    assert pytest.approx(result) == result_scipy
