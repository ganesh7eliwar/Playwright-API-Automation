"""
This test verifies the /products/:productId endpoint which returns details of a single product.
Expected behavior: the API should respond with HTTP 200 when a valid productId is provided,
and return a JSON object containing fields such as id (integer), category (string), name (string), and inStock (boolean).
If an invalid productId is requested, the API should return HTTP 404 Not Found.
"""
# Importing json for reading/writing JSON files, random for selecting a random product, pytest for test framework, and Loggen for logging
from utilities.logger import Loggen
import json, pytest, random

# Initialize the logger for this test module
log = Loggen.log_generator()


@pytest.mark.product
# The test function uses pytest fixtures: api_context (for making API calls) and data_dir (for test data file paths)
def test_get_a_product(api_context, data_dir):
    log.info("Starting test: test_get_a_product - Retrieving details of a single product.")

    # Read and load the list of all products from the test data JSON file
    log.info("Loading product list from test data file.")
    with open(data_dir / 'simple_grocery_store_get_all_products.json', 'r') as f:
        product_list = json.load(f)

    # Randomly select a product ID from the available products for diverse test coverage
    log.info("Selecting random product from available products.")
    product_id = random.choice(product_list)['id']
    log.debug(f"Selected product ID: {product_id}")

    # Write the extracted product ID to a text file for potential debugging or reuse
    log.info("Saving selected product ID to file for reuse.")
    with open(data_dir / 'simple_grocery_store_productId.txt', 'w') as f:
        f.write(str(product_id))

    # Make a GET request to retrieve the details of the specific product
    log.info("Making GET request to retrieve product details.")
    response = api_context.get(f"/products/{product_id}")

    # Parse the JSON response to get the product details
    log.info("Parsing response from get product endpoint.")
    product = response.json()

    # Assert that the response is OK and the status is 200 (OK) indicating the product was found
    log.info("Asserting that get product endpoint returned 200 OK.")
    assert response.ok, 'Expected 200 OK but got an error response.'
    assert response.status == 200, 'API response is not equal to 200.'

    # Type checks - ensure each field in the product has the correct data type
    log.info("Performing type checks on product fields.")
    assert isinstance(product["id"], int), f'Product id should be an integer. got {type(product["id"])}.'
    assert isinstance(product["category"], str), f'Category should be a string. got {type(product["category"])}.'
    assert isinstance(product["name"], str), f'Name should be a string. got {type(product["name"])}.'
    assert isinstance(product["manufacturer"],
                      str), f'Manufacturer should be a string. got {type(product["manufacturer"])}.'
    assert isinstance(product["price"], float), f'Product price should be float. got {type(product["price"])}.'
    assert isinstance(product["current-stock"],
                      int), f'Product current-stock should be int. got {type(product["current-stock"])}.'
    assert isinstance(product["inStock"], bool), f'inStock should be a boolean. got {type(product["inStock"])}.'

    # Save the product details to a JSON file for potential debugging or reuse in other tests
    log.info("Saving product details to JSON file for debugging and reuse.")
    with open(data_dir / 'simple_grocery_store_product_details.json', 'w') as f:
        json.dump(product, f, indent=4)

    log.info("✓ Test completed successfully: Product details retrieved.")
