"""
This endpoint (PATCH /orders/:orderId) updates an existing order for the authenticated API client.
The request body must be in JSON format and can optionally include 'customerName' or 'comment'
to modify those fields. The Authorization header with a valid bearer token is required, and the
orderId must be specified in the path.

Example request body:
{
    "customerName": "Joe Doe"
}

Possible responses:
- 204 No Content: Order updated successfully.
- 400 Bad Request: Invalid parameters provided in the request body.
- 401 Unauthorized: Authentication failed (invalid or missing bearer token).
- 404 Not Found: No order exists with the specified orderId for the API client.

Usage: Call PATCH /orders/:orderId with the Authorization header, orderId, and optional JSON body
to update details of an existing order.
"""
from utilities.logger import Loggen
import json, pytest, random

# Initialize the logger for this test module
log = Loggen.log_generator()


@pytest.mark.order(9)  # Ensure this test runs after the order is created
@pytest.mark.e2e
@pytest.mark.slow  # This test may take longer due to reading files and making API calls
# The test function uses pytest fixtures: api_context (for making API calls) and data_dir (for test data file paths)
def test_update_an_order(api_context, data_dir):
    log.info("Starting test: test_update_an_order - Updating an existing order.")

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

    # Prepare the payload to update the customer name of the order
    log.info("Preparing update payload.")
    payload = {"comment": f"Bring the Order by {random.randint(1, 5)}:00 PM"}
    log.debug(f"Update payload: {payload}")

    # Make a PATCH request to update the existing order with the new customer name
    log.info("Making PATCH request to update order.")
    response = api_context.patch(
        f"/orders/{order_id}", data=payload,
        headers={"Authorization": f"Bearer {access_token['accessToken']}"}
    )

    # Assert that the response status is 204 (No Content) indicating successful update of the order
    log.info("Asserting that update order endpoint returned 204 No Content.")
    assert response.status == 204, f'Expected 204 No Content but got {response.status}.'
    log.info("✓ Test completed successfully: Order updated.")
