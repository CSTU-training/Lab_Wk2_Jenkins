from app.calculator import add, divide


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-2, -3) == -5


def test_divide_numbers():
    assert divide(10, 2) == 5
