"""
This test validates the /products endpoint which returns a list of items from the inventory.
It checks that the API responds with HTTP 200 and returns a JSON array of products.
Optional query parameters (category, results, available) can be used to filter the response.
A correct response should include product details such as id, category, name, and inStock status.
"""
# Importing json for reading/writing JSON files, pytest for test framework, and Loggen for logging
from utilities.logger import Loggen
import json, pytest

# Initialize the logger for this test module
log = Loggen.log_generator()


@pytest.mark.product
# The test function uses pytest fixtures: api_context (for making API calls) and data_dir (for test data file paths)
def test_get_all_products(api_context, data_dir):
    log.info("Starting test: test_get_all_products - Retrieving all products from inventory.")

    # Make a GET request to retrieve all products from the inventory
    log.info("Making GET request to retrieve all products.")
    response = api_context.get("/products")

    # Parse the JSON response to get the list of products
    log.info("Parsing response from get all products endpoint.")
    data = response.json()

    # Extract the first product from the list for validation checks
    log.info("Extracting first product for validation.")
    product = data[0]
    log.debug(f"First product ID: {product.get('id', 'N/A')}")

    # Save the complete list of all products to a JSON file for use by other tests
    log.info("Saving all products to JSON file for reuse by other tests.")
    with open(data_dir / 'simple_grocery_store_get_all_products.json', 'w') as f:
        json.dump(data, f, indent=4)
    log.debug(f"Saved {len(data)} products to file.")

    # Assert that the response is OK and the status is 200 (OK)
    log.info("Asserting that get all products endpoint returned 200 OK.")
    assert response.ok, 'Expected 200 OK but got an error response.'
    assert response.status == 200, 'API response is not equal to 200.'

    # Assert that required fields exist in the first product
    log.info("Asserting that products contain required fields.")
    assert "id" in product, 'Product should contain an "id" field.'
    assert "name" in product, 'Product should contain a "name" field.'
    assert "inStock" in product, 'Product should contain a "inStock" field.'

    # Validate that the response contains at least one product
    log.info("Asserting that response contains at least one product.")
    assert len(data) > 0, 'Expected at least one product in the response.'

    # Type checks - ensure the response structure and fields have correct data types
    log.info("Performing type checks on response structure.")
    assert isinstance(data, list), 'Response should be a list of products.'
    assert isinstance(product["id"], int), f'Product id should be int, got {type(product["id"])}.'
    assert isinstance(product["inStock"], bool), f'Product inStock should be boolean, got {type(product["inStock"])}.'

    log.info("✓ Test completed successfully: All products retrieved.")
