"""
Integration tests for FastAPI endpoints in main.py
Tests all API endpoints with various scenarios
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create test client
client = TestClient(app)


class TestRootEndpoint:
    """Test cases for the root endpoint"""
    
    def test_root_endpoint_success(self):
        """Test root endpoint returns HTML calculator interface"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert b"FastAPI Calculator" in response.content
        
    def test_root_endpoint_structure(self):
        """Test API info endpoint response structure"""
        response = client.get("/api")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["endpoints"], dict)
        assert "/" in data["endpoints"]
        assert "/docs" in data["endpoints"]
        assert "/calculate" in data["endpoints"]


class TestHealthEndpoint:
    """Test cases for the health check endpoint"""
    
    def test_health_endpoint_success(self):
        """Test health endpoint returns healthy status"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        
    def test_health_endpoint_response_type(self):
        """Test health endpoint returns JSON"""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"


class TestCalculateEndpointAddition:
    """Test cases for addition operations"""
    
    def test_add_positive_numbers(self):
        """Test adding two positive numbers"""
        payload = {"num1": 10, "num2": 5, "operation": "add"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 15.0
        assert data["operation"] == "add"
        assert data["num1"] == 10.0
        assert data["num2"] == 5.0
        
    def test_add_negative_numbers(self):
        """Test adding negative numbers"""
        payload = {"num1": -10, "num2": -5, "operation": "add"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        assert response.json()["result"] == -15.0
        
    def test_add_with_zero(self):
        """Test adding with zero"""
        payload = {"num1": 10, "num2": 0, "operation": "add"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        assert response.json()["result"] == 10.0
        
    def test_add_decimal_numbers(self):
        """Test adding decimal numbers"""
        payload = {"num1": 10.5, "num2": 5.5, "operation": "add"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        assert response.json()["result"] == 16.0
        
    def test_add_case_insensitive(self):
        """Test operation is case insensitive"""
        payload = {"num1": 10, "num2": 5, "operation": "ADD"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        assert response.json()["result"] == 15.0


class TestCalculateEndpointSubtraction:
    """Test cases for subtraction operations"""
    
    def test_subtract_positive_numbers(self):
        """Test subtracting positive numbers"""
        payload = {"num1": 10, "num2": 5, "operation": "subtract"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        assert response.json()["result"] == 5.0
        
    def test_subtract_negative_result(self):
        """Test subtraction resulting in negative number"""
        payload = {"num1": 5, "num2": 10, "operation": "subtract"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        assert response.json()["result"] == -5.0
        
    def test_subtract_negative_numbers(self):
        """Test subtracting negative numbers"""
        payload = {"num1": -10, "num2": -5, "operation": "subtract"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        assert response.json()["result"] == -5.0
        
    def test_subtract_with_zero(self):
        """Test subtracting zero"""
        payload = {"num1": 10, "num2": 0, "operation": "subtract"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        assert response.json()["result"] == 10.0


class TestCalculateEndpointMultiplication:
    """Test cases for multiplication operations"""
    
    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers"""
        payload = {"num1": 10, "num2": 5, "operation": "multiply"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        assert response.json()["result"] == 50.0
        
    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers"""
        payload = {"num1": -10, "num2": -5, "operation": "multiply"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        assert response.json()["result"] == 50.0
        
    def test_multiply_with_zero(self):
        """Test multiplying with zero"""
        payload = {"num1": 10, "num2": 0, "operation": "multiply"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        assert response.json()["result"] == 0.0
        
    def test_multiply_decimals(self):
        """Test multiplying decimal numbers"""
        payload = {"num1": 2.5, "num2": 4, "operation": "multiply"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        assert response.json()["result"] == 10.0


class TestCalculateEndpointDivision:
    """Test cases for division operations"""
    
    def test_divide_positive_numbers(self):
        """Test dividing positive numbers"""
        payload = {"num1": 10, "num2": 5, "operation": "divide"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        assert response.json()["result"] == 2.0
        
    def test_divide_with_remainder(self):
        """Test division with remainder"""
        payload = {"num1": 10, "num2": 3, "operation": "divide"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        result = response.json()["result"]
        assert abs(result - 3.333333) < 0.0001
        
    def test_divide_negative_numbers(self):
        """Test dividing negative numbers"""
        payload = {"num1": -10, "num2": -5, "operation": "divide"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        assert response.json()["result"] == 2.0
        
    def test_divide_by_zero(self):
        """Test division by zero returns error"""
        payload = {"num1": 10, "num2": 0, "operation": "divide"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 400
        assert "Cannot divide by zero" in response.json()["detail"]
        
    def test_divide_zero_by_number(self):
        """Test dividing zero by a number"""
        payload = {"num1": 0, "num2": 5, "operation": "divide"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        assert response.json()["result"] == 0.0


class TestCalculateEndpointErrors:
    """Test cases for error handling"""
    
    def test_invalid_operation(self):
        """Test invalid operation returns error"""
        payload = {"num1": 10, "num2": 5, "operation": "power"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 400
        assert "Invalid operation" in response.json()["detail"]
        
    def test_missing_num1(self):
        """Test missing num1 parameter"""
        payload = {"num2": 5, "operation": "add"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 422  # Validation error
        
    def test_missing_num2(self):
        """Test missing num2 parameter"""
        payload = {"num1": 10, "operation": "add"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 422
        
    def test_missing_operation(self):
        """Test missing operation parameter"""
        payload = {"num1": 10, "num2": 5}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 422
        
    def test_invalid_num1_type(self):
        """Test invalid type for num1"""
        payload = {"num1": "abc", "num2": 5, "operation": "add"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 422
        
    def test_invalid_num2_type(self):
        """Test invalid type for num2"""
        payload = {"num1": 10, "num2": "xyz", "operation": "add"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 422
        
    def test_empty_operation_string(self):
        """Test empty operation string"""
        payload = {"num1": 10, "num2": 5, "operation": ""}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 400
        
    def test_empty_payload(self):
        """Test empty payload"""
        response = client.post("/calculate", json={})
        assert response.status_code == 422


class TestCalculateEndpointResponseStructure:
    """Test cases for response structure validation"""
    
    def test_response_contains_all_fields(self):
        """Test response contains all required fields"""
        payload = {"num1": 10, "num2": 5, "operation": "add"}
        response = client.post("/calculate", json=payload)
        data = response.json()
        assert "result" in data
        assert "operation" in data
        assert "num1" in data
        assert "num2" in data
        
    def test_response_field_types(self):
        """Test response field types are correct"""
        payload = {"num1": 10, "num2": 5, "operation": "add"}
        response = client.post("/calculate", json=payload)
        data = response.json()
        assert isinstance(data["result"], float)
        assert isinstance(data["operation"], str)
        assert isinstance(data["num1"], float)
        assert isinstance(data["num2"], float)


class TestCalculateEndpointEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_very_large_numbers(self):
        """Test calculation with very large numbers"""
        payload = {"num1": 10**100, "num2": 10**100, "operation": "add"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        
    def test_very_small_numbers(self):
        """Test calculation with very small numbers"""
        payload = {"num1": 1e-10, "num2": 1e-10, "operation": "add"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        
    def test_mixed_integer_and_float(self):
        """Test calculation with mixed integer and float"""
        payload = {"num1": 10, "num2": 5.5, "operation": "add"}
        response = client.post("/calculate", json=payload)
        assert response.status_code == 200
        assert response.json()["result"] == 15.5


class TestNonExistentEndpoints:
    """Test non-existent endpoints return 404"""
    
    def test_invalid_endpoint(self):
        """Test accessing non-existent endpoint"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
        
    def test_wrong_method(self):
        """Test using wrong HTTP method"""
        response = client.get("/calculate")
        assert response.status_code == 405  # Method not allowed
