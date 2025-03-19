import pytest
from decimal import Decimal
from app.core.calculation import Calculation
from app.math_operations import operations

def test_calculation_initialization():
    calc = Calculation(Decimal('2'), Decimal('3'), 'add')
    assert calc.a == Decimal('2')
    assert calc.b == Decimal('3')
    assert calc.operation_name == 'add'
    assert calc.operation == operations['add']
    assert calc.result == Decimal('5')

def test_calculation_repr():
    calc = Calculation(Decimal('2'), Decimal('3'), 'add')
    assert repr(calc) == "Calculation(2, 3, add, 5)"

def test_calculation_perform():
    calc = Calculation(Decimal('2'), Decimal('3'), 'add')
    assert calc.perform() == Decimal('5')

def test_calculation_invalid_operation():
    with pytest.raises(TypeError):
        Calculation(Decimal('2'), Decimal('3'), 'invalid_operation')

def test_calculation_from_history():
    calc = Calculation.from_history('2', '3', 'add', '5')
    assert calc.a == Decimal('2')
    assert calc.b == Decimal('3')
    assert calc.operation_name == 'add'
    assert calc.result == Decimal('5')
