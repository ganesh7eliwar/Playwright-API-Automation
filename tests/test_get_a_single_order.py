"""
This endpoint (GET /orders/:orderId) retrieves the details of a single order
associated with the authenticated API client. The request must include a valid
Authorization header with the bearer token, and the orderId must be provided
in the path. An optional query parameter 'invoice' can be set to true to return
the PDF invoice for the order.

Possible responses:
- 200 OK: Successfully returns the order details.
- 401 Unauthorized: The request is not authenticated (invalid or missing bearer token).
- 404 Not Found: No order exists with the specified orderId for the API client.

Usage: Call GET /orders/:orderId with the Authorization header and orderId to
fetch details of a specific order, optionally including the invoice.
"""
import json
from utilities.logger import Loggen

# Initialize the logger for this test module
log = Loggen.log_generator()


# The test function uses pytest fixtures: api_context (for making API calls) and data_dir (for test data file paths)
def test_get_a_single_order(api_context, data_dir):
    log.info("Starting test: test_get_a_single_order - Retrieving details of a single order.")

    # Read the last generated access token from a JSON file (created by test_register_a_new_api_client)
    log.info("Reading access token from file.")
    with open(data_dir / 'simple_grocery_store_last_generated_access_token.json', 'r') as f:
        access_token = json.load(f)

    # Read the last created order details from a JSON file (created by test_create_a_new_order)
    log.info("Reading order details from file.")
    with open(data_dir / 'simple_grocery_store_order_details.json', 'r') as f:
        order_details = json.load(f)

    order_id = order_details['orderId']
    log.debug(f"Using order ID: {order_id}")

    # Make a GET request to retrieve the details of the specific order
    log.info("Making GET request to retrieve single order details.")
    response = api_context.get(f"/orders/{order_id}",
                               headers={"Authorization": f"Bearer {access_token['accessToken']}"})

    # Assert that the response status is 200 (OK) indicating successful retrieval of the order
    log.info("Asserting that get single order endpoint returned 200 OK.")
    assert response.status == 200, f'Expected 200 OK but got {response.status}.'

    # Parse the JSON response to get the order details
    log.info("Parsing response from get single order endpoint.")
    order = response.json()

    # Save the order details to a JSON file for potential debugging or reuse in other tests
    log.info("Saving single order details to JSON file for debugging and reuse.")
    with open(data_dir / 'simple_grocery_store_single_order_details.json', 'w') as f:
        json.dump(order, f, indent=4)

    log.info("✓ Test completed successfully: Single order details retrieved.")
