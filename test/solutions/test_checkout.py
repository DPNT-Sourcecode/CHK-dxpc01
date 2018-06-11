import pytest
from lib.solutions.checkout import checkout


@pytest.mark.parametrize(('skus', 'result'), (
        ('', 0),
        ('A', 50),
        ('AA', 100),
        ('AAA', 130),
        ('D', 15),
        ('BBAAA', 175),
        ('AAAAACD', 235),
        ('AAAAAAAAACD', 415),
        ('BBE', 85),
        ('BBEE', 110),
        ('BFF', 50),
        ('FBFF', 50)
))
def test_checkout_success(skus, result):
    assert checkout(skus) == result


@pytest.mark.parametrize('skus', (
        '12',
        True,
        object(),
        'BBA1'
))
def test_checkout_fails(skus):
    assert checkout(skus) == -1, 'Must return -1 for skus {}'.format(skus)
