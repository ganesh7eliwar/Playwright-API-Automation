# Simple Grocery Store API Automation Framework

[![pytest](https://img.shields.io/badge/pytest-9.0.2-blue.svg)](https://pytest.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.58.0-green.svg)](https://playwright.dev/)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)

A comprehensive API automation testing framework for the Simple Grocery Store REST API, built with pytest and Playwright.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Environment Configuration](#environment-configuration)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Best Practices](#best-practices)
- [Future Improvements](#future-improvements)

## 🎯 Project Overview

This project provides automated API testing for the Simple Grocery Store REST API. The framework validates all core API endpoints including:

- **Authentication**: API client registration and token management
- **Products**: Product catalog retrieval and individual product details
- **Carts**: Shopping cart creation, item management, and cart operations
- **Orders**: Order creation, retrieval, updates, and deletion

The framework is designed to ensure API reliability, validate response schemas, and catch regressions through comprehensive test coverage.

## 🛠 Tech Stack

### Core Testing Framework
- **pytest 9.0.2** - Testing framework with fixtures and plugins
- **Playwright 1.58.0** - Browser automation library used for API testing
- **pytest-playwright 0.7.2** - Integration between pytest and Playwright

### Data Generation & Utilities
- **Faker 40.11.0** - Generate realistic test data
- **requests 2.32.5** - HTTP library (used by Playwright internally)

### Development Tools
- **Python 3.12+** - Programming language
- **certifi, charset-normalizer, urllib3** - HTTP handling dependencies
- **colorama, Pygments** - Terminal output formatting

## 📁 Project Structure

```text
Simple_Grocery_Store_API/
├── LICENSE                            # MIT license for repository use
├── README.md                          # Project overview, setup, and documentation
├── Jenkinsfile                        # CI/CD pipeline definition
├── pytest.ini                         # pytest configuration and options
├── requirements.txt                   # Python package dependencies
├── Simple_Grocery_Store_Data/         # Persisted API data and test fixtures
├── tests/                             # pytest test suite and fixtures
├── utilities/                         # Reusable helper modules
├── docs/                              # Optional project and test documentation
├── reports/                           # Optional test reports and output artifacts
└── src/                               # Optional source modules for helpers or clients
```

### Folder Details

- **`LICENSE`**: MIT License file for the codebase and contributor use.
- **`README.md`**: Project purpose, setup instructions, structure, and best practices.
- **`Jenkinsfile`**: Build and automation pipeline definition for CI environments.
- **`pytest.ini`**: Configuration for pytest behavior, markers, and reporting.
- **`requirements.txt`**: Pinning of required Python packages and library versions.
- **`Simple_Grocery_Store_Data/`**: Persistent API response files, payloads, IDs, and test artifacts.
- **`tests/`**: End-to-end pytest coverage for API endpoints, test cases, and fixtures.
- **`utilities/`**: Shared helper code and logger utilities for stable test execution.
- **`docs/`**: Recommended place for additional documentation such as design notes, process guides, and architecture details.
- **`reports/`**: Recommended location for HTML reports, logs, and CI artifacts generated during test execution.
- **`src/`**: Recommended location for reusable automation modules, API clients, or shared library code.

### Current Implementation Summary

- `tests/`: Includes pytest test files for carts, orders, products, status checks, and client registration.
- `Simple_Grocery_Store_Data/`: Contains sample JSON payloads, saved API responses, and runtime artifacts used across the suite.
- `utilities/`: Includes the project logger used for consistent test output and troubleshooting.

## 🚀 Setup and Installation

### Prerequisites

- **Python 3.12+** installed on your system
- **pip** package manager
- **Git** for cloning the repository

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Simple_Grocery_Store_API
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers** (required for API testing)
   ```bash
   playwright install
   ```

5. **Verify installation**
   ```bash
   pytest --version
   playwright --version
   ```

## ⚙️ Environment Configuration

### API Endpoint

The framework is configured to test against the Simple Grocery Store API:

- **Base URL**: `https://simple-grocery-store-api.click`
- **API Type**: REST API
- **Authentication**: Bearer token-based

### Configuration Details

The framework uses pytest fixtures defined in `tests/conftest.py`:

- **`api_context`**: Session-scoped Playwright API request context
- **`data_dir`**: Path to test data directory for file operations

### Test Data Management

Tests store and retrieve data using JSON files in the `Simple_Grocery_Store_Data/` directory:

- **Access tokens**: Stored after client registration
- **Cart IDs**: Generated during cart creation tests
- **Product data**: Cached from API responses
- **Order details**: Saved after order creation

## 🧪 Running Tests

### Basic Test Execution

Run all tests:
```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v
```

Run a specific test file:
```bash
pytest tests/test_get_status.py -v
```

### Test Execution Options

**Run tests with different verbosity levels:**
```bash
pytest -q          # Quiet mode
pytest -v          # Verbose mode
pytest -vv         # Very verbose mode
```

**Run tests with output capture:**
```bash
pytest -s          # Don't capture output (show print statements)
pytest --tb=short  # Short traceback format
pytest --tb=line   # Line-only traceback
```

**Run tests with color output:**
```bash
pytest --color=yes
```

### Test Selection and Filtering

**Run tests by name pattern:**
```bash
pytest -k "status"           # Run tests containing "status"
pytest -k "cart and add"     # Run tests containing both "cart" and "add"
pytest -k "not slow"         # Run tests not marked as slow
```

**Run tests by directory:**
```bash
pytest tests/                # Run all tests in tests directory
```

**Run tests with markers** (when implemented):
```bash
pytest -m smoke              # Run smoke tests
pytest -m regression         # Run regression tests
```

### Parallel Test Execution

**Run tests in parallel** (requires `pytest-xdist`):
```bash
pip install pytest-xdist
pytest -n auto               # Use all CPU cores
pytest -n 4                  # Use 4 workers
```

### Example Test Commands

```bash
# Quick health check
pytest tests/test_get_status.py -v

# Run authentication tests
pytest tests/test_register_a_new_api_client.py -v

# Run all cart-related tests
pytest -k "cart" -v

# Run tests with detailed output
pytest tests/test_get_all_products.py -vv -s
```

## 📊 Test Coverage

The framework provides comprehensive coverage of the Simple Grocery Store API:

### Authentication (1 test)
- API client registration and token generation

### Products (2 tests)
- Retrieve all products
- Get individual product details

### Carts (6 tests)
- Create new shopping cart
- Add items to cart
- Get cart details and items
- Modify cart items
- Replace cart items
- Delete items from cart

### Orders (5 tests)
- Create new orders
- Get all orders
- Get single order details
- Update existing orders
- Delete orders

### Health Check (1 test)
- API status verification

**Total: 15 test files covering all major API endpoints**

## ✅ Best Practices Followed

### Code Organization
- **Clear naming conventions**: Test files follow `test_<action>_<resource>.py` pattern
- **Separation of concerns**: Tests, fixtures, and data are properly separated
- **Modular structure**: Each test file focuses on a specific API endpoint

### Test Design
- **Descriptive docstrings**: Each test includes detailed documentation
- **Comprehensive assertions**: Tests validate status codes, response structure, and data types
- **Realistic test data**: Uses Faker library for generating varied test inputs

### Framework Architecture
- **Fixture-based setup**: Uses pytest fixtures for reusable test components
- **Session management**: Proper API context management with cleanup
- **Data persistence**: Test data stored in structured JSON format

### Documentation
- **Inline comments**: Code includes explanatory comments
- **API documentation**: Tests document expected request/response formats
- **Error handling**: Tests include appropriate error messages

## 🔮 Future Improvements

### Test Framework Enhancements
- **pytest-order integration**: Implement test execution ordering for dependent tests
- **Parallel execution**: Enable safe parallel test runs with proper isolation
- **Test parameterization**: Add parametrized tests for better coverage

### Code Quality Improvements
- **API client classes**: Create dedicated client classes for better abstraction
- **Schema validation**: Implement JSON schema validation for responses
- **Error handling**: Add retry logic and better error reporting

### Infrastructure & CI/CD
- **Environment configuration**: Support multiple test environments (dev/staging/prod)
- **CI/CD pipeline**: Implement automated testing with GitHub Actions
- **Test reporting**: Add HTML reports and test metrics

### Test Coverage Expansion
- **Negative test cases**: Add tests for error scenarios and edge cases
- **Performance testing**: Include response time validation
- **Load testing**: Add tests for API performance under load

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-test`)
3. Commit your changes (`git commit -am 'Add new test'`)
4. Push to the branch (`git push origin feature/new-test`)
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or issues:
- Create an issue in the repository
- Review the test documentation in individual test files
- Check the REVIEW_ANALYSIS.md for detailed framework recommendations

---

**Framework Version**: 1.0.0
**Last Updated**: April 21, 2026
**Python Version**: 3.12+
**API Under Test**: Simple Grocery Store API</content>
<filePath>C:\Users\ganes\PycharmProjects\API_Automation\Simple_Grocery_Store_API\README.md
