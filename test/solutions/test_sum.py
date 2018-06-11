import pytest

from lib.solutions.sum import sum


@pytest.mark.parametrize(('x', 'y', 'result'), (
        (0, 0, 0),
        (0, 1, 1),
        (1, 2, 3)
))
def test_sum_success(x, y, result):
    assert sum(x, y) == result
