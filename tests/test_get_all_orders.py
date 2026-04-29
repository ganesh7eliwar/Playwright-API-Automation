"""
This endpoint (GET /orders) retrieves all orders created by the authenticated API client.
A valid Authorization header containing the bearer token must be included in the request.

Possible responses:
- 200 OK: Successfully returns the list of orders associated with the client.
- 401 Unauthorized: The request is not authenticated (invalid or missing bearer token).

Usage: Call GET /orders with the Authorization header to fetch all orders for the client.
"""
# Importing json for handling JSON data, pytest for the test framework, and Loggen for logging
from utilities.logger import Loggen
import json, pytest

# Initialize the logger for this test module
log = Loggen.log_generator()


@pytest.mark.order(10)  # Ensure this test runs after the order is created and updated
@pytest.mark.e2e
@pytest.mark.slow  # This test may take longer due to reading files and making API calls
# The test function uses pytest fixtures: api_context (for making API calls) and data_dir (for test data file paths)
def test_get_all_orders(api_context, data_dir):
    log.info("Starting test: test_get_all_orders - Retrieving all orders for authenticated client.")

    # Read the last generated access token from a JSON file (created by test_register_a_new_api_client)
    log.info("Reading access token from file.")
    with open(data_dir / 'simple_grocery_store_last_generated_access_token.json', 'r') as f:
        access_token = json.load(f)

    # Make a GET request to retrieve all orders for the authenticated client
    log.info("Making GET request to retrieve all orders.")
    response = api_context.get("/orders", headers={"Authorization": f"Bearer {access_token['accessToken']}"})

    # Assert that the response status is 200 (OK) indicating successful retrieval of orders
    log.info("Asserting that get all orders endpoint returned 200 OK.")
    assert response.status == 200, f'Expected 200 OK but got {response.status}.'

    # Parse the JSON response to get the list of orders
    log.info("Parsing response from get all orders endpoint.")
    orders = response.json()
    log.debug(f"Retrieved {len(orders)} orders.")

    # Save the list of orders to a JSON file for potential debugging or reuse in other tests
    log.info("Saving all orders to JSON file for debugging and reuse.")
    with open(data_dir / 'simple_grocery_store_get_all_orders.json', 'w') as f:
        json.dump(orders, f, indent=4)

    log.info("✓ Test completed successfully: All orders retrieved.")
