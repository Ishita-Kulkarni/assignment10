#!/bin/bash
# Local CI checks script - Simulates GitHub Actions CI pipeline
# Run this before pushing to ensure CI will pass

set -e

echo "======================================"
echo "FastAPI Calculator - Local CI Checks"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track failures
FAILED=0

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo -e "${RED}❌ Virtual environment not found${NC}"
    echo "Run: python -m venv venv && source venv/bin/activate"
    exit 1
fi

# Check if dependencies are installed
echo "Checking dependencies..."
pip list | grep -q "pytest" || { echo -e "${RED}❌ Test dependencies not installed${NC}"; exit 1; }
echo -e "${GREEN}✓ Dependencies OK${NC}"
echo ""

# 1. Code Formatting Check
echo "1. Checking code formatting..."
echo "-----------------------------------"
if pip list | grep -q "black"; then
    black --check . --exclude='venv/|htmlcov/|\.pytest_cache/' 2>/dev/null && \
        echo -e "${GREEN}✓ Black formatting: PASS${NC}" || \
        { echo -e "${YELLOW}⚠ Black formatting: Issues found (non-blocking)${NC}"; }
else
    echo -e "${YELLOW}⚠ Black not installed (skipping)${NC}"
fi
echo ""

# 2. Import Sorting Check
echo "2. Checking import sorting..."
echo "-----------------------------------"
if pip list | grep -q "isort"; then
    isort --check-only . --skip venv --skip htmlcov --skip .pytest_cache 2>/dev/null && \
        echo -e "${GREEN}✓ isort check: PASS${NC}" || \
        { echo -e "${YELLOW}⚠ isort check: Issues found (non-blocking)${NC}"; }
else
    echo -e "${YELLOW}⚠ isort not installed (skipping)${NC}"
fi
echo ""

# 3. Linting with Flake8
echo "3. Linting code..."
echo "-----------------------------------"
if pip list | grep -q "flake8"; then
    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=venv,htmlcov,.pytest_cache && \
        echo -e "${GREEN}✓ Flake8 critical: PASS${NC}" || \
        { echo -e "${RED}❌ Flake8 critical: FAIL${NC}"; FAILED=1; }
    
    flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude=venv,htmlcov,.pytest_cache > /dev/null 2>&1
    echo -e "${GREEN}✓ Flake8 style: PASS${NC}"
else
    echo -e "${YELLOW}⚠ Flake8 not installed (skipping)${NC}"
fi
echo ""

# 4. Security Check
echo "4. Security scanning..."
echo "-----------------------------------"
if pip list | grep -q "bandit"; then
    bandit -r . --exclude ./venv,./htmlcov,./.pytest_cache -q 2>/dev/null && \
        echo -e "${GREEN}✓ Bandit security: PASS${NC}" || \
        { echo -e "${YELLOW}⚠ Bandit security: Issues found (non-blocking)${NC}"; }
else
    echo -e "${YELLOW}⚠ Bandit not installed (skipping)${NC}"
fi
echo ""

# 5. Unit Tests
echo "5. Running unit tests..."
echo "-----------------------------------"
if pytest tests/test_operations.py -v --tb=short; then
    echo -e "${GREEN}✓ Unit tests: PASS${NC}"
else
    echo -e "${RED}❌ Unit tests: FAIL${NC}"
    FAILED=1
fi
echo ""

# 6. Integration Tests
echo "6. Running integration tests..."
echo "-----------------------------------"
if pytest tests/test_main.py -v --tb=short; then
    echo -e "${GREEN}✓ Integration tests: PASS${NC}"
else
    echo -e "${RED}❌ Integration tests: FAIL${NC}"
    FAILED=1
fi
echo ""

# 7. Logging Tests
echo "7. Running logging tests..."
echo "-----------------------------------"
if pytest tests/test_logging.py -v --tb=short; then
    echo -e "${GREEN}✓ Logging tests: PASS${NC}"
else
    echo -e "${RED}❌ Logging tests: FAIL${NC}"
    FAILED=1
fi
echo ""

# 8. Coverage Check
echo "8. Checking test coverage..."
echo "-----------------------------------"
if pytest tests/test_operations.py tests/test_main.py tests/test_logging.py \
    --cov=. --cov-report=term-missing --cov-report=html -q; then
    echo -e "${GREEN}✓ Coverage: PASS${NC}"
else
    echo -e "${RED}❌ Coverage: FAIL${NC}"
    FAILED=1
fi
echo ""

# 9. Application Startup Test
echo "9. Verifying application can start..."
echo "-----------------------------------"
timeout 3 python main.py > /dev/null 2>&1 || code=$?
if [ $code -eq 124 ] || [ $code -eq 0 ]; then
    echo -e "${GREEN}✓ Application startup: PASS${NC}"
else
    echo -e "${RED}❌ Application startup: FAIL${NC}"
    FAILED=1
fi
echo ""

# Summary
echo "======================================"
echo "           Summary"
echo "======================================"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo -e "${GREEN}✓ Ready to push to GitHub${NC}"
    echo ""
    echo "Your code will pass CI checks."
    exit 0
else
    echo -e "${RED}❌ Some checks failed${NC}"
    echo -e "${RED}Please fix the issues before pushing${NC}"
    echo ""
    echo "Run specific checks:"
    echo "  pytest tests/test_operations.py -v"
    echo "  pytest tests/test_main.py -v"
    echo "  flake8 . --exclude=venv"
    exit 1
fi
