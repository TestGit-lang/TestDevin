import pytest
from sample import check_prime_number


@pytest.mark.parametrize(
    ('number', 'expected'), 
    [
        pytest.param(1,  False, id="test1"),
        pytest.param(2,  False, id="test2"),
        pytest.param(3,  False, id="test3"),
        pytest.param(4,  False, id="test4"),
        pytest.param(5,  False, id="test5"),
        pytest.param(6,  False, id="test6"),
        pytest.param(7,  False, id="test7"),
        pytest.param(8,  False, id="test8"),
        pytest.param(9,  False, id="test9"),
        pytest.param(10, False, id="test10"),
    ]
)

def test_is_prime(number, expected):
    assert check_prime_number(number) == expected