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

```
Simple_Grocery_Store_API/
├── requirements.txt                    # Python dependencies
├── REVIEW_ANALYSIS.md                  # Framework review and recommendations
├── Simple_Grocery_Store_Data/          # Test data storage
│   ├── simple_grocery_store_all_client_details.json
│   ├── simple_grocery_store_all_orders.json
│   ├── simple_grocery_store_cart_details.json
│   ├── simple_grocery_store_get_all_products.json
│   ├── simple_grocery_store_get_cart_items.json
│   ├── simple_grocery_store_last_added_item_to_cart.json
│   ├── simple_grocery_store_last_created_cart_details.json
│   ├── simple_grocery_store_last_created_cartId.txt
│   ├── simple_grocery_store_last_created_client_details.json
│   ├── simple_grocery_store_last_generated_access_token.json
│   ├── simple_grocery_store_order_details.json
│   ├── simple_grocery_store_product_details.json
│   ├── simple_grocery_store_productId.txt
│   ├── simple_grocery_store_single_order_details.json
│   └── simple_grocery_store_status.json
└── tests/
    ├── __init__.py
    ├── conftest.py                     # pytest fixtures and configuration
    ├── test_add_item_to_cart.py
    ├── test_create_a_new_order.py
    ├── test_create_new_cart.py
    ├── test_delete_an_order.py
    ├── test_delete_item_from_cart.py
    ├── test_get_a_cart.py
    ├── test_get_a_product.py
    ├── test_get_a_single_order.py
    ├── test_get_all_orders.py
    ├── test_get_all_products.py
    ├── test_get_cart_items.py
    ├── test_get_status.py
    ├── test_modify_item_in_cart.py
    ├── test_register_a_new_api_client.py
    ├── test_replace_item_from_cart.py
    ├── test_update_an_order.py
    └── __pycache__/
```

### Key Directories Explained

- **`tests/`**: Contains all test files and pytest configuration
  - `conftest.py`: Defines fixtures for API context and test data management
  - Individual test files follow naming pattern `test_<action>_<resource>.py`

- **`Simple_Grocery_Store_Data/`**: Stores test data and API responses
  - JSON files contain API response data for test verification
  - Text files store IDs and tokens for test dependencies
  - Files are generated during test execution

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
