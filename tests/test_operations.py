"""
Unit tests for operations.py
Tests all calculator functions individually
"""
import pytest
from app.operations import (
    add, subtract, multiply, divide, calculate,
    DivisionByZeroError, InvalidOperationError
)


class TestAddition:
    """Test cases for add function"""
    
    def test_add_positive_numbers(self):
        """Test adding two positive numbers"""
        assert add(5, 3) == 8
        assert add(10.5, 2.5) == 13.0
        
    def test_add_negative_numbers(self):
        """Test adding two negative numbers"""
        assert add(-5, -3) == -8
        assert add(-10.5, -2.5) == -13.0
        
    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers"""
        assert add(5, -3) == 2
        assert add(-5, 3) == -2
        
    def test_add_with_zero(self):
        """Test adding with zero"""
        assert add(0, 5) == 5
        assert add(5, 0) == 5
        assert add(0, 0) == 0
        
    def test_add_large_numbers(self):
        """Test adding large numbers"""
        assert add(1000000, 2000000) == 3000000
        
    def test_add_decimal_numbers(self):
        """Test adding decimal numbers"""
        result = add(0.1, 0.2)
        assert abs(result - 0.3) < 1e-10


class TestSubtraction:
    """Test cases for subtract function"""
    
    def test_subtract_positive_numbers(self):
        """Test subtracting positive numbers"""
        assert subtract(10, 3) == 7
        assert subtract(5.5, 2.5) == 3.0
        
    def test_subtract_negative_numbers(self):
        """Test subtracting negative numbers"""
        assert subtract(-5, -3) == -2
        assert subtract(-10, -15) == 5
        
    def test_subtract_mixed_numbers(self):
        """Test subtracting with mixed signs"""
        assert subtract(5, -3) == 8
        assert subtract(-5, 3) == -8
        
    def test_subtract_with_zero(self):
        """Test subtracting with zero"""
        assert subtract(5, 0) == 5
        assert subtract(0, 5) == -5
        assert subtract(0, 0) == 0
        
    def test_subtract_same_numbers(self):
        """Test subtracting same numbers"""
        assert subtract(7, 7) == 0
        assert subtract(-5, -5) == 0


class TestMultiplication:
    """Test cases for multiply function"""
    
    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers"""
        assert multiply(5, 3) == 15
        assert multiply(2.5, 4) == 10.0
        
    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers"""
        assert multiply(-5, -3) == 15
        assert multiply(-2, -4) == 8
        
    def test_multiply_mixed_signs(self):
        """Test multiplying with mixed signs"""
        assert multiply(5, -3) == -15
        assert multiply(-5, 3) == -15
        
    def test_multiply_with_zero(self):
        """Test multiplying with zero"""
        assert multiply(5, 0) == 0
        assert multiply(0, 5) == 0
        assert multiply(0, 0) == 0
        
    def test_multiply_with_one(self):
        """Test multiplying with one"""
        assert multiply(5, 1) == 5
        assert multiply(1, 5) == 5
        
    def test_multiply_decimals(self):
        """Test multiplying decimal numbers"""
        assert multiply(2.5, 4) == 10.0
        assert multiply(0.5, 0.5) == 0.25


class TestDivision:
    """Test cases for divide function"""
    
    def test_divide_positive_numbers(self):
        """Test dividing positive numbers"""
        assert divide(10, 2) == 5
        assert divide(15, 3) == 5
        assert divide(7.5, 2.5) == 3.0
        
    def test_divide_negative_numbers(self):
        """Test dividing negative numbers"""
        assert divide(-10, -2) == 5
        assert divide(-15, -3) == 5
        
    def test_divide_mixed_signs(self):
        """Test dividing with mixed signs"""
        assert divide(10, -2) == -5
        assert divide(-10, 2) == -5
        
    def test_divide_by_zero(self):
        """Test division by zero raises exception"""
        with pytest.raises(DivisionByZeroError) as exc_info:
            divide(10, 0)
        assert "Cannot divide by zero" in str(exc_info.value)
        
    def test_divide_zero_by_number(self):
        """Test dividing zero by a number"""
        assert divide(0, 5) == 0
        assert divide(0, -5) == 0
        
    def test_divide_by_one(self):
        """Test dividing by one"""
        assert divide(5, 1) == 5
        assert divide(-5, 1) == -5
        
    def test_divide_decimals(self):
        """Test dividing decimal numbers"""
        assert divide(5, 2) == 2.5
        assert divide(1, 3) == pytest.approx(0.333333, rel=1e-5)


class TestCalculate:
    """Test cases for the main calculate function"""
    
    def test_calculate_add(self):
        """Test calculate with add operation"""
        assert calculate(5, 3, "add") == 8
        assert calculate(5, 3, "ADD") == 8  # Test case insensitivity
        
    def test_calculate_subtract(self):
        """Test calculate with subtract operation"""
        assert calculate(10, 3, "subtract") == 7
        assert calculate(10, 3, "SUBTRACT") == 7
        
    def test_calculate_multiply(self):
        """Test calculate with multiply operation"""
        assert calculate(5, 3, "multiply") == 15
        assert calculate(5, 3, "MULTIPLY") == 15
        
    def test_calculate_divide(self):
        """Test calculate with divide operation"""
        assert calculate(10, 2, "divide") == 5
        assert calculate(10, 2, "DIVIDE") == 5
        
    def test_calculate_invalid_operation(self):
        """Test calculate with invalid operation"""
        with pytest.raises(InvalidOperationError) as exc_info:
            calculate(5, 3, "power")
        assert "Invalid operation" in str(exc_info.value)
        assert "power" in str(exc_info.value)
        
    def test_calculate_division_by_zero(self):
        """Test calculate with division by zero"""
        with pytest.raises(DivisionByZeroError):
            calculate(10, 0, "divide")
            
    def test_calculate_empty_operation(self):
        """Test calculate with empty operation"""
        with pytest.raises(InvalidOperationError):
            calculate(5, 3, "")
            
    def test_calculate_special_characters(self):
        """Test calculate with special characters in operation"""
        with pytest.raises(InvalidOperationError):
            calculate(5, 3, "add@#$")


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_very_large_numbers(self):
        """Test operations with very large numbers"""
        large_num = 10**100
        assert add(large_num, large_num) == 2 * large_num
        assert subtract(large_num, large_num) == 0
        
    def test_very_small_numbers(self):
        """Test operations with very small numbers"""
        small_num = 1e-10
        assert add(small_num, small_num) == pytest.approx(2e-10)
        
    def test_negative_zero(self):
        """Test operations with negative zero"""
        assert add(-0, 5) == 5
        assert multiply(-0, 5) == 0
        
    def test_infinity_operations(self):
        """Test operations with infinity"""
        inf = float('inf')
        assert add(inf, 5) == inf
        assert multiply(inf, 2) == inf
        assert subtract(inf, 5) == inf
        
    def test_nan_operations(self):
        """Test operations with NaN"""
        import math
        nan = float('nan')
        result = add(nan, 5)
        assert math.isnan(result)
