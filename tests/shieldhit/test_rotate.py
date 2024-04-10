from converter.common import rotate, format_float
from scipy.spatial.transform import Rotation
import pytest


@pytest.mark.parametrize('vector,angles', [([1, 0, 0], [90, 0, 0]), ([0, 1, 0], [270, 0, 0]), ([1, 0, 0], [90, 90, 90]),
                                           ([0, 0, 0], [45, 45, 45]), ([2, 3, 4], [30, 45, 60]),
                                           ([1, 1, 1], [-45, -30, -60]), ([1, 1, 1], [270, 180, 360]),
                                           ([-1, -2, -3], [45, 45, 45]), ([0, 1, 1], [45, 0, 0]),
                                           ([2, 4, -7], [23, -82, 213])])
def test_rotate(vector, angles, precision=8):
    """Test the rotate function with various inputs. Expects angles as degrees"""
    # Rotate using custom function
    result = rotate(vector, angles)

    # Rotate using SciPy
    r = Rotation.from_euler('xyz', angles, degrees=True)
    result_scipy = r.apply(vector)

    for idx, element in enumerate(result):
        assert format_float(element, precision) == format_float(
            result_scipy[idx], precision
        ), f'Expected {format_float(result_scipy[idx], precision)}, but got {format_float(element, precision)}'
