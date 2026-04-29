"""
This test verifies the /carts/:cartId/items/:itemId endpoint which allows replacing
an existing item in the cart with a new product definition.
Expected behavior:
When a valid cartId, itemId, and productId are provided in the JSON body,
the API should return HTTP 204 No Content, indicating the item was replaced successfully.
If the request body is invalid or missing required parameters, the API should return HTTP 400 Bad Request.
If the cart or item does not exist, the API should return HTTP 404 Not Found.
"""
# Importing json for reading JSON files, random for selecting random items/products
from utilities.logger import Loggen
import json, pytest, random

log = Loggen.log_generator()


@pytest.mark.order(6)  # Ensure this test runs after items have been added to the cart
@pytest.mark.e2e
@pytest.mark.slow # This test may take longer due to reading files and making multiple API calls
# The test function uses pytest fixtures: api_context (for making API calls) and data_dir (for test data file paths)
def test_replace_item_in_cart(api_context, data_dir):
    log.info("Starting test: test_replace_item_in_cart - Replacing an item in the cart with a new product.")
    # Read the last created cart ID from a file (created by test_create_new_cart)
    log.info("Reading cart ID from file.")
    with open(data_dir / 'simple_grocery_store_last_created_cartId.txt', 'r') as f:
        cart_id = str(f.read().strip())  # strip() removes any extra spaces/newlines

    # Read the list of items currently in the cart and extract their product IDs
    log.info("Reading cart items from file.")
    with open(data_dir / 'simple_grocery_store_get_cart_items.json', 'r') as f:
        cart_items = json.load(f)
        # Randomly select an item ID from the cart to replace
        log.info("Selecting random item from cart to replace.")
        item_id = str(random.choice(cart_items)['id'])
        # Extract a list of all productIds currently in the cart
        log.info("Extracting product IDs of items currently in the cart.")
        products_in_cart = [item['productId'] for item in cart_items]

    # Read the list of all available products and filter for in-stock items
    log.info("Loading product list from test data file and filtering for in-stock products.")
    with open(data_dir / 'simple_grocery_store_get_all_products.json', 'r') as f:
        product_list = json.load(f)
        # Create a list of productIds that are in stock
        log.info("Extracting product IDs of in-stock products.")
        product_ids = [product['id'] for product in product_list if product['inStock']]

    # Remove products already in the cart from the available products list to avoid duplicates
    log.info("Removing products already in the cart from the list of available products.")
    for product in products_in_cart:
        if product in product_ids:
            product_ids.remove(product)

    # Select a random product ID from the remaining available products
    log.info("Selecting a random product ID from the available products to replace the item in the cart.")
    product_id = random.choice(product_ids)

    # Prepare the payload with the new product ID and a random quantity (between 2 and 5)
    log.info("Preparing payload with new product ID and random quantity.")
    payload = {"productId": product_id, "quantity": int(random.randint(2, 5))}

    # Only proceed with the replacement if the cart has items
    log.info("Checking if cart has items before attempting to replace an item.")
    if cart_items:
        # Make a PUT request to replace the item with the new product
        log.info("Making PUT request to replace the item in the cart.")
        response = api_context.put(f'/carts/{cart_id}/items/{item_id}', data=payload)

        # Assert that the response status is 204 (No Content) indicating successful replacement
        log.info("Asserting that replace item endpoint returned 204 No Content.")
        assert response.status == 204, f'Expected 204 No Content but got {response.status}.'
        log.info("✓ Test completed successfully: Item replaced in cart.")

    else:
        # If the cart is empty, return a message indicating no items to replace
        log.info("Cart is empty, skipping item replacement test.")
        return 'Cart is Empty.'
