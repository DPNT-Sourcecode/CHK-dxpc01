import pytest
from lib.solutions.checkout import checkout


@pytest.mark.parametrize(('skus', 'result'), (
        ('AA', 100),
        ('AAA', 130),
        ('D', 15),
        ('BBAAA', 175),
        ('AAAAACD', 265)
))
def test_checkout_success(skus, result):
    assert checkout(skus) == result


@pytest.mark.parametrize('skus', (
        ('Z',),
        ('AAA',),
        ('D',),
        ('BBAAA',),
        ('AAAAACD',)
))
def test_checkout_faile(skus):
    assert checkout(skus) == -1
