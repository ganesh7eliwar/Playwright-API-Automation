"""
This test verifies the /carts endpoint which creates a new shopping cart.
Expected behavior: submitting an empty POST request should return HTTP 201 Created
along with a JSON response containing a unique cartId.
The cartId will be used in subsequent requests (e.g., adding items to the cart).
"""
# Importing json for reading/writing JSON files, pytest for test framework, and Loggen for logging
from utilities.logger import Loggen
import json, pytest

# Initialize the logger for this test module
log = Loggen.log_generator()


# This test should run after the API status check to ensure the API is up before attempting to create a cart
@pytest.mark.order(2)
@pytest.mark.e2e
# The test function uses pytest fixtures: api_context (for making API calls) and data_dir (for test data file paths)
def test_create_new_cart(api_context, data_dir):
    log.info("Starting test: test_create_new_cart - Creating a new shopping cart.")

    # Make a POST request to the /carts endpoint to create a new shopping cart
    log.info("Making POST request to /carts endpoint to create new cart.")
    response = api_context.post("/carts")

    # Parse the JSON response to get the cart details
    log.info("Parsing response from /carts endpoint.")
    cart = response.json()

    # Assert that the response status is 201 (Created) indicating successful cart creation
    log.info("Asserting that the /carts endpoint returned 201 Created.")
    assert response.status == 201, f"Expected 201 Created but got {response.status}"

    # Assert that the response is a dictionary (JSON object)
    log.info("Asserting that response is a JSON object.")
    assert isinstance(cart, dict), "Response should be a JSON object."

    # Assert that the response contains the required fields for a valid cart
    log.info("Asserting that response contains required cart fields.")
    assert "cartId" in cart, "Response should contain a cartId."
    assert "created" in cart, "Response should contain 'created'."

    # Type checks - ensure each field has the correct data type
    log.info("Performing type checks on cart fields.")
    assert isinstance(cart["cartId"], str), f"cartId should be a string, got {type(cart['cartId'])}."
    assert isinstance(cart["created"], bool), f"created should be a boolean, got {type(cart['created'])}."

    # Value check - ensure the 'created' field is True, indicating the cart was successfully created
    log.info("Asserting that cart was successfully created.")
    assert cart["created"] is True, "Expected 'created' to be True."

    # Save the complete cart response to a JSON file for potential debugging or reuse in other tests
    log.info("Saving cart details to JSON file for debugging and reuse.")
    with open(data_dir / 'simple_grocery_store_cart_details.json', 'w') as f:
        json.dump(cart, f, indent=4)

    # Save the cartId to a separate text file for quick access by subsequent tests that need it
    log.info("Saving cartId to text file for quick access by other tests.")
    with open(data_dir / 'simple_grocery_store_last_created_cartId.txt', 'w') as f:
        f.write(str(cart["cartId"]))

    log.info("✓ Test completed successfully: New shopping cart created.")
