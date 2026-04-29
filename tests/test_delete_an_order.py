"""
This endpoint (DELETE /orders/:orderId) deletes an existing order associated with the
authenticated API client. The request must include a valid Authorization header with
the bearer token, and the orderId must be specified in the path. No request body is
required for deletion.

Possible responses:
- 204 No Content: Order deleted successfully.
- 400 Bad Request: Invalid parameters provided (e.g., malformed orderId).
- 401 Unauthorized: Authentication failed (invalid or missing bearer token).
- 404 Not Found: No order exists with the specified orderId for the API client.

Usage: Call DELETE /orders/:orderId with the Authorization header and orderId to
remove a specific order from the system.
"""
import json, random
from utilities.logger import Loggen

# Initialize the logger for this test module
log = Loggen.log_generator()


# The test function uses pytest fixtures: api_context (for making API calls) and data_dir (for test data file paths)
def test_delete_an_order(api_context, data_dir):
    log.info("Starting test: test_delete_an_order - Deleting an existing order.")

    # Read the last generated access token from a JSON file (created by test_register_a_new_api_client)
    log.info("Reading all orders from file.")
    all_orders = data_dir / 'simple_grocery_store_all_orders.json'
    with open(all_orders, 'r') as f:
        orders = json.load(f)

    # Read the last generated access token from a JSON file (created by test_register_a_new_api_client)
    log.info("Reading access token from file.")
    with open(data_dir / 'simple_grocery_store_last_generated_access_token.json', 'r') as f:
        access_token = json.load(f)

    # Ensure there are orders available to delete before proceeding
    log.info("Asserting that orders are available for deletion.")
    assert orders, "No orders available to delete."
    log.debug(f"Found {len(orders)} orders available.")

    # Randomly select an order ID from the list of orders for test coverage
    log.info("Selecting random order for deletion.")
    order_id = random.choice(orders)['id']
    log.debug(f"Selected order ID for deletion: {order_id}")

    # Make a DELETE request to remove the specified order using the API client fixture
    log.info("Making DELETE request to remove order.")
    response = api_context.delete(
        f"/orders/{order_id}",
        headers={"Authorization": f"Bearer {access_token['accessToken']}"}
    )

    # Assert that the response status is 204 (No Content) indicating successful deletion of the order
    log.info("Asserting that delete order endpoint returned 204 No Content.")
    assert response.status == 204, f'Expected 204 No Content but got {response.status}.'
    log.info("✓ Test completed successfully: Order deleted.")
