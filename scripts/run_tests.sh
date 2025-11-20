#!/bin/bash
# Script to run all tests with different categories

set -e

echo "======================================"
echo "FastAPI Calculator Test Suite"
echo "======================================"
echo ""

# Activate virtual environment
source venv/bin/activate

# Run unit tests
echo "Running Unit Tests..."
echo "--------------------------------------"
pytest tests/test_operations.py -v --tb=short
echo ""

# Run integration tests
echo "Running Integration Tests..."
echo "--------------------------------------"
pytest tests/test_main.py -v --tb=short
echo ""

# Run all tests with coverage
echo "Running All Tests with Coverage..."
echo "--------------------------------------"
pytest tests/test_operations.py tests/test_main.py -v --cov=. --cov-report=term-missing --cov-report=html
echo ""

echo "======================================"
echo "Test Summary"
echo "======================================"
echo "✓ Unit tests completed"
echo "✓ Integration tests completed"
echo "✓ Coverage report generated in htmlcov/"
echo ""
echo "To run E2E tests, start the server and run:"
echo "  pytest tests/test_e2e.py -v"
echo ""
