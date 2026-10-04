import pytest
from src import calculator

def test_fun1():
    assert calculator.fun1(2, 3) == 5
    assert calculator.fun1(5,0) == 5
    assert calculator.fun1 (-1, 1) == 0
    assert calculator.fun1 (-1, -1) == -2


def test_fun2():
    assert calculator.fun2(2, 3) == -1
    assert calculator.fun2(5,0) == 5
    assert calculator.fun2 (-1, 1) == -2
    assert calculator.fun2 (-1, -1) == 0

def test_fun3():
    assert calculator.fun3(2, 3) == 6
    assert calculator.fun3(5,0) == 0
    assert calculator.fun3 (-1, 1) == -1
    
    assert calculator.fun3 (-1, -1) == 1

def test_fun4():
    assert calculator.fun4(2, 3, 5) == 10
    assert calculator.fun4(5,0, -1) == 4
    assert calculator.fun4 (-1, -1, -1) == -3
    
    assert calculator.fun4 (-1, -1, 100) == 98

def test_fun4_with_floats():
    assert calculator.fun4(1.5, 2.5, 1) == 5.0


def test_float_addition_needs_tolerance():
    # 0.1 + 0.2 is 0.30000000000000004 in floating point, so compare approximately
    assert calculator.fun1(0.1, 0.2) == pytest.approx(0.3)


def test_fun4_rejects_non_numbers():
    with pytest.raises(ValueError):
        calculator.fun4("a", 2, 3)
    with pytest.raises(ValueError):
        calculator.fun4(1, "b", 3)
    with pytest.raises(ValueError):
        calculator.fun4(1, 2, "c")


def test_fun1_fun2_fun3_reject_non_numbers():
    with pytest.raises(ValueError):
        calculator.fun1("2", 3)
    with pytest.raises(ValueError):
        calculator.fun2(1, None)
    with pytest.raises(ValueError):
        calculator.fun3(1, [2])



    
