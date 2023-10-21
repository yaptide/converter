import pytest
from converter.shieldhit.geo import format_float


@pytest.mark.parametrize("value,n,expected", [
    (1, 10, 1.0),
    (0, 10, 0.0),
    (-1, 10, -1.0),
    (1.0/3, 10, 0.33333333),
    (-1.0/3, 10, -0.3333333),
    (123+1.0/3, 10, 123.333333),
    (-(123+1.0/3), 10, -123.33333),
])
def test_format_float(value, n, expected):
    """Test if format_float works on all the edge cases."""
    assert format_float(value, n) == expected


def test_format_float_large_example():
    """Test if format float will raise an exception when given bad arguments."""
    with pytest.raises(ValueError):
        format_float(1000000, 2)
