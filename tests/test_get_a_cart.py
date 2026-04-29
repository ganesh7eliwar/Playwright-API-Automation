"""
This test verifies the /carts/:cartId endpoint which retrieves the details of a specific cart.
Expected behavior: when a valid cartId is provided, the API should return HTTP 200 OK
along with a JSON object containing the cart details (e.g., items, cartId).
If an invalid or non‑existent cartId is requested, the API should return HTTP 404 Not Found.
"""
# Importing json for reading/writing JSON files, pytest for test framework, and Loggen for logging
from utilities.logger import Loggen
import json, pytest

# Initialize the logger for this test module
log = Loggen.log_generator()


# This test should run after the cart creation test since it depends on having a valid cartId to retrieve cart details
# @pytest.mark.order(after="create_cart")
# @pytest.mark.e2e
# @pytest.mark.dependency(name="get_cart_by_id", depends=["create_cart"])
# The test function uses pytest fixtures: api_context (for making API calls) and data_dir (for test data file paths)
def test_get_cart_by_id(api_context, data_dir):
    log.info("Starting test: test_get_cart_by_id - Retrieving details of a specific cart.")

    # Read the last created cart ID from a file (created by test_create_new_cart)
    log.info("Reading cart ID from file.")
    with open(data_dir / 'simple_grocery_store_last_created_cartId.txt', 'r') as f:
        cart_id = f.read().strip()  # strip() removes any extra spaces/newlines
    log.debug(f"Using cart ID: {cart_id}")

    # Make a GET request to retrieve the details of the specific cart
    log.info("Making GET request to retrieve cart details.")
    response = api_context.get(f"/carts/{cart_id}")

    # Assert that the response status is 200 (OK) indicating the cart was found
    log.info("Asserting that get cart endpoint returned 200 OK.")
    assert response.status == 200, f"Expected 200 Created but got {response.status}"

    # Parse the JSON response to get the cart details
    log.info("Parsing response from get cart endpoint.")
    cart = response.json()

    # Assert that the response contains the required fields for a valid cart
    log.info("Asserting that response contains required cart fields.")
    assert 'items' in cart, 'Response should contain items.'
    assert 'created' in cart, 'Response should contain created.'

    # Type checks - ensure each field has the correct data type
    log.info("Performing type checks on cart fields.")
    assert isinstance(cart['items'], list), f'Response should be a list of products. got {type(cart["items"])}.'
    assert isinstance(cart, dict), 'Response should be a JSON object.'

    # Save the cart details to a JSON file for potential debugging or reuse in other tests
    log.info("Saving cart details to JSON file for debugging and reuse.")
    with open(data_dir / 'simple_grocery_store_last_created_cart_details.json', 'w') as f:
        json.dump(cart, f, indent=4)

    log.info("✓ Test completed successfully: Cart details retrieved.")
