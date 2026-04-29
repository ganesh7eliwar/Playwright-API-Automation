"""
This test verifies the /carts/:cartId/items/:itemId endpoint which allows modifying
information about an existing item in the cart.
Expected behavior: when a valid cartId, itemId, and quantity are provided in the JSON body,
the API should return HTTP 204 No Content, indicating the item was updated successfully.
If the request body is invalid or missing required parameters, the API should return HTTP 400 Bad Request.
If the cart or item does not exist, the API should return HTTP 404 Not Found.
"""
# Importing json for reading JSON files, random for selecting random items/values, pytest for test framework, and Loggen for logging
from utilities.logger import Loggen
import json, pytest, random

# Initialize the logger for this test module
log = Loggen.log_generator()


@pytest.mark.order(5)  # Ensure this test runs after items have been added to the cart
@pytest.mark.e2e
@pytest.mark.slow  # This test may take longer due to reading files and making multiple API calls
# The test function uses pytest fixtures: api_context (for making API calls) and data_dir (for test data file paths)
def test_modify_item_in_cart(api_context, data_dir):
    log.info("Starting test: test_modify_item_in_cart - Modifying quantity of an item in the cart.")

    # Read the last created cart ID from a file (created by test_create_new_cart)
    log.info("Reading cart ID from file.")
    with open(data_dir / 'simple_grocery_store_last_created_cartId.txt', 'r') as f:
        cart_id = str(f.read().strip())  # strip() removes any extra spaces/newlines
    log.debug(f"Using cart ID: {cart_id}")

    # Read the list of items currently in the cart from a JSON file (populated by test_get_cart_items)
    log.info("Reading cart items from file.")
    with open(data_dir / 'simple_grocery_store_get_cart_items.json', 'r') as f:
        item_list = json.load(f)
        log.debug(f"Found {len(item_list)} items in cart.")

    # Randomly select an item ID from the list to modify
    log.info("Selecting random item from cart to modify.")
    item_id = str(random.choice(item_list)['id'])
    log.debug(f"Selected item ID for modification: {item_id}")

    # Prepare the payload with a new quantity value (randomly selected between 2 and 5)
    log.info("Preparing payload with new quantity value.")
    quantity = {
        "quantity": int(random.randint(2, 5))
    }
    log.debug(f"New quantity: {quantity['quantity']}")

    # Only proceed with the modification if the cart has items
    if item_list:
        log.info("Cart has items, proceeding with modification.")
        # Make a PATCH request to update the quantity of the selected item
        log.info("Making PATCH request to modify item quantity.")
        response = api_context.patch(f"/carts/{cart_id}/items/{item_id}", data=quantity)

        # Assert that the response status is 204 (No Content) indicating successful modification
        log.info("Asserting that modify item endpoint returned 204 No Content.")
        assert response.status == 204, f'Expected 204 No Content but got {response.status}'
        log.info("✓ Test completed successfully: Item quantity modified.")
    else:
        # If the cart is empty, return a message indicating no items to modify
        log.warning("Cart is empty, skipping item modification test.")
        return 'Cart is Empty'
