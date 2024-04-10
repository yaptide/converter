from converter.common import rotate
from scipy.spatial.transform import Rotation
from converter.common import format_float
import pytest


@pytest.mark.parametrize(
    'vector,angles',
    [
        ([1, 0, 0], [90, 0, 0]),
        ([0, 1, 0], [270, 0, 0]),
        # Add more test cases here
    ])
def test_rotate(vector, angles, precision=8):
    """Test the rotate function with various inputs. Expects angles as degrees"""

    # Rotate using custom function
    result = rotate(vector, angles)

    # Rotate using SciPy
    r = Rotation.from_euler('xyz', angles, degrees=True)
    result_scipy = r.apply(vector)

    for i in range(len(result)):
        assert format_float(result[i], precision) == format_float(
            result_scipy[i], precision
        ), f'Expected {format_float(result_scipy[i], precision)}, but got {format_float(result[i], precision)}'
