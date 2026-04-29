"""
This endpoint (POST /orders) is used to create a new order from an existing cart.
The request body must be JSON and include the cartId and customerName.
Optionally, a comment can be added. The Authorization header must contain
a valid bearer token for the API client.
Once the order is successfully submitted, the associated cart is deleted.
Example request body:
{
    "cartId": "ZFe4yhG5qNhmuNyrbLWa4",
    "customerName": "John Doe"
}
Possible responses:
- 201 Created: Order created successfully
- 400 Bad Request: Invalid parameters provided
- 401 Unauthorized: Authentication failed (check bearer token)
"""
# Importing json for handling JSON data, pytest for the test framework, and Loggen for logging
from utilities.logger import Loggen
import json, pytest

# Initialize the logger for this test module
log = Loggen.log_generator()


@pytest.mark.order(8)  # Ensure this test runs after the cart is created and client is registered
@pytest.mark.e2e
@pytest.mark.slow  # This test may take longer due to reading files and making API calls
# The test function uses pytest fixtures: api_context (for making API calls) and data_dir (for test data file paths)
def test_create_a_new_order(api_context, data_dir):
    log.info("Starting test: test_create_a_new_order - Creating a new order from cart.")

    # Read the last created cart ID from a file (created by test_create_new_cart)
    log.info("Reading cart ID from file.")
    with open(data_dir / 'simple_grocery_store_last_created_cartId.txt', 'r') as f:
        cart_id = str(f.read().strip())  # strip() removes any extra spaces/newlines
    log.debug(f"Using cart ID: {cart_id}")

    log.info("Reading access token from file.")
    with open(data_dir / 'simple_grocery_store_last_generated_access_token.json', 'r') as f:
        access_token = json.load(f)

    log.info("Reading client details from file.")
    with open(data_dir / 'simple_grocery_store_last_created_client_details.json', 'r') as f:
        client_details = json.load(f)
    log.debug(f"Using customer name: {client_details['clientName']}")

    # Prepare the payload with the cart ID and a customer name for order creation
    log.info("Preparing order payload.")
    payload = {"cartId": cart_id, "customerName": client_details['clientName']}
    log.debug(f"Order payload: {payload}")

    # Make a POST request to create a new order using the specified cart ID and customer name
    log.info("Making POST request to create new order.")
    response = api_context.post(
        "/orders", data=payload,
        headers={"Authorization": f"Bearer {access_token['accessToken']}"}
    )

    # Assert that the response status is 201 (Created) indicating successful order creation
    log.info("Asserting that create order endpoint returned 201 Created.")
    assert response.status == 201, f'Expected 201 Created but got {response.status}.'

    # Parse the JSON response to get the order details
    log.info("Parsing response from create order endpoint.")
    order_details = response.json()

    # Save the order details to a JSON file for potential debugging or reuse in other tests
    log.info("Saving order details to JSON file for debugging and reuse.")
    with open(data_dir / 'simple_grocery_store_order_details.json', 'w') as f:
        json.dump(order_details, f, indent=4)

    log.info("✓ Test completed successfully: New order created.")
