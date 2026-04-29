"""
This test verifies the /carts/:cartId/items/:itemId endpoint which allows deleting
an existing item from the cart.
Expected behavior:
When a valid cartId and itemId are provided, the API should return HTTP 204 No Content,
indicating the item was deleted successfully.
If the cart or item does not exist, the API should return HTTP 404 Not Found.
"""
# Importing json for reading JSON files, random for selecting a random item, pytest for test framework, and Loggen for logging
from utilities.logger import Loggen
import json, random

# Initialize the logger for this test module
log = Loggen.log_generator()


# The test function uses pytest fixtures: api_context (for making API calls) and data_dir (for test data file paths)
def test_delete_item_from_cart(api_context, data_dir):
    log.info("Starting test: test_delete_item_from_cart - Deleting an item from the cart.")
    
    # Read the last created cart ID from a file (created by a previous test or setup)
    log.info("Reading cart ID from file.")
    with open(data_dir / 'simple_grocery_store_last_created_cartId.txt', 'r') as f:
        cart_id = str(f.read().strip())  # strip() removes any extra spaces/newlines
    log.debug(f"Using cart ID: {cart_id}")

    # Read the list of items currently in the cart from a JSON file (populated by test_get_cart_items)
    log.info("Reading cart items from file.")
    with open(data_dir / 'simple_grocery_store_get_cart_items.json', 'r') as f:
        item_list = json.load(f)
        log.debug(f"Found {len(item_list)} items in cart.")
        
        # Randomly select an item ID from the list of items in the cart
        if item_list:
            item_id = str(random.choice(item_list)['id'])
            log.debug(f"Selected item ID for deletion: {item_id}")

    # Make a DELETE request to remove the selected item from the cart
    log.info("Making DELETE request to remove item from cart.")
    response = api_context.delete(f'/carts/{cart_id}/items/{item_id}')

    # Assert that the response status is 204 (No Content) indicating successful deletion
    log.info("Asserting that delete item endpoint returned 204 No Content.")
    assert response.status == 204, f'Expected 204 No Content but got {response.status}.'
    log.info("✓ Test completed successfully: Item deleted from cart.")
