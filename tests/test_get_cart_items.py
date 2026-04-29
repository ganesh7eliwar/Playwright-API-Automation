"""
This test verifies the /carts/:cartId/items endpoint which retrieves all items in a specific cart.
Expected behavior: when a valid cartId is provided, the API should return HTTP 200 OK
along with a JSON array containing the items currently in the cart.
Each item should include fields such as productId (int) and quantity (int).
If an invalid or non‑existent cartId is requested, the API should return HTTP 404 Not Found.
"""
# Importing json for reading/writing JSON files, random for selecting a random item, pytest for test framework, and Loggen for logging
from utilities.logger import Loggen
import json, pytest, random

# Initialize the logger for this test module
log = Loggen.log_generator()


# This test should run after the cart creation test since it depends on having a valid cartId to retrieve cart items
@pytest.mark.order(4)  # Ensure this test runs after items have been added to the cart
@pytest.mark.e2e
# The test function uses pytest fixtures: api_context (for making API calls) and data_dir (for test data file paths)
def test_get_cart_items(api_context, data_dir):
    log.info("Starting test: test_get_cart_items - Retrieving all items from the shopping cart.")

    # Read the last created cart ID from a file (created by test_create_new_cart)
    log.info("Reading cart ID from file.")
    with open(data_dir / 'simple_grocery_store_last_created_cartId.txt', 'r') as f:
        cart_id = f.read().strip()
    log.debug(f"Using cart ID: {cart_id}")

    # Make a GET request to retrieve all items in the specific cart
    log.info("Making GET request to retrieve cart items.")
    response = api_context.get(f'/carts/{cart_id}/items')

    # Assert that the response status is 200 (OK) indicating the cart items were retrieved
    log.info("Asserting that get cart items endpoint returned 200 OK.")
    assert response.status == 200, f'Expected 200 Created but got {response.status}.'

    # Parse the JSON response to get the list of items
    log.info("Parsing response from get cart items endpoint.")
    items = response.json()

    # Type check - ensure the response is a list
    log.info("Asserting that response is a list of items.")
    assert isinstance(items, list), f'Response should be a list of products. got {type(items)}.'
    log.debug(f"Retrieved {len(items)} items from cart.")

    # Validate the structure of cart items only if the cart contains items
    if items:  # validate structure only if cart has items
        log.info("Cart contains items, validating item structure.")
        # Select a random item from the list to validate its structure
        item = items[random.randint(0, len(items) - 1)]

        # Assert that each item contains the required fields
        log.info("Asserting that items contain required fields.")
        assert 'productId' in item, 'Item should contain productId.'
        assert 'quantity' in item, 'Item should contain quantity.'

        # Type checks - ensure each field has the correct data type
        log.info("Performing type checks on item fields.")
        assert isinstance(item['productId'], int), f"productId should be an integer. got {type(item['productId'])}"
        assert isinstance(item['quantity'], int), f"quantity should be an integer. got {type(item['quantity'])}"
    else:
        log.info("Cart is empty, skipping item structure validation.")

    # Save the list of cart items to a JSON file for use by other tests (e.g., delete, modify, replace item)
    log.info("Saving cart items to JSON file for debugging and reuse.")
    with open(data_dir / 'simple_grocery_store_get_cart_items.json', 'w') as f:
        json.dump(items, f, indent=4)

    log.info("✓ Test completed successfully: Cart items retrieved.")
