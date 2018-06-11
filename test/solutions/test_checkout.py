import pytest

@pytest.mark.parametrize(('skus', 'result'), (
        ('AA', 100),
        ('AAA', 130)
))
def test_checkout_success(skus, result):
    assert sum(skus) == result
