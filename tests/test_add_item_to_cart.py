"""
This test verifies the /carts/:cartId/items endpoint which allows adding a single item to an existing cart.
Expected behavior: when a valid cartId and productId are provided in the JSON body,
the API should return HTTP 201 Created along with confirmation that the item was added.
If no quantity is specified, the default value should be 1.
If an invalid cartId is provided, the API should return HTTP 404 Not Found.
"""
# Importing json for reading/writing JSON files, random for selecting a random product, pytest for test framework, and Loggen for logging
from utilities.logger import Loggen
import json, pytest, random

# Initialize the logger for this test module
log = Loggen.log_generator()


# This test should run after the cart creation test since it depends on having a valid cartId to add items to the cart
@pytest.mark.order(3)
@pytest.mark.e2e
# The test function uses pytest fixtures: api_context (for making API calls) and data_dir (for test data file paths)
def test_add_item_to_cart(api_context, data_dir):
    log.info("Starting test: test_add_item_to_cart - Adding an item to the shopping cart.")

    # Open and load the list of all products from the test data JSON file
    log.info("Loading product list from test data file.")
    with open(data_dir / "simple_grocery_store_get_all_products.json", "r", encoding="utf-8") as f:
        product_list = json.load(f)

    # Ensure the product list is not empty before proceeding
    log.info("Asserting that product list is not empty.")
    assert product_list, "Product list is empty; cannot select a product."

    # Randomly select a product ID from the available products for test coverage
    log.info("Selecting random product from available products.")
    product_id = random.choice(product_list)["id"]
    log.debug(f"Selected product ID: {product_id}")

    # Prepare the payload for the API request (only productId, quantity defaults to 1)
    log.info("Preparing payload with selected product ID.")
    payload = {
        "productId": product_id
    }

    # Read the last created cart ID from a file (created by a previous test or setup)
    log.info("Reading cart ID from file.")
    with open(data_dir / "simple_grocery_store_last_created_cartId.txt", "r", encoding="utf-8") as f:
        cart_id = f.read().strip()  # strip() removes any extra spaces/newlines

    # Ensure the cart ID is present before making the API call
    log.info("Asserting that cart ID is present.")
    assert cart_id, "Cart ID is empty."
    log.debug(f"Using cart ID: {cart_id}")

    # Make a POST request to add the item to the cart using the API context fixture
    log.info("Making POST request to add item to cart.")
    response = api_context.post(f'/carts/{cart_id}/items', data=payload)

    # Parse the JSON response from the API
    log.info("Parsing response from add item to cart endpoint.")
    item = response.json()

    # Assert that the response status code is 201 (Created)
    log.info("Asserting that add item endpoint returned 201 Created.")
    assert response.status == 201, f'Expected 201 Created but got {response.status}.'

    # Validate that the response contains the required fields
    log.info("Asserting that response contains required fields.")
    assert 'created' in item, 'Response should contain created.'
    assert 'itemId' in item, 'Response should contain items.'

    # Check that the response is a dictionary (JSON object)
    log.info("Asserting that response is a JSON object.")
    assert isinstance(item, dict), 'Response should be a JSON object.'

    # Check that the 'created' field is a boolean value
    log.info("Performing type checks on response fields.")
    assert isinstance(item['created'], bool), f'Response should be a list of products. got {type(item["created"])}.'
    # Check that the 'itemId' field is an integer
    assert isinstance(item['itemId'], int), f'Response should be a list of products. got {type(item["itemId"])}.'

    # Save the API response to a file for possible reuse in other tests or debugging
    log.info("Saving added item details to JSON file for debugging and reuse.")
    with open(data_dir / 'simple_grocery_store_last_added_item_to_cart.json', 'w') as f:
        json.dump(item, f, indent=4)

    log.info("✓ Test completed successfully: Item added to cart.")
