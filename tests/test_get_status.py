"""
This test verifies the health of the API by calling the /status endpoint.
Expected behavior: the API should respond with HTTP 200 and return {"status": "UP"}.
If the response is missing or different, it indicates the API is not functioning correctly.
"""
# Importing json for reading/writing JSON files, pytest for test framework, and Loggen for logging
from utilities.logger import Loggen
import json, pytest

# Initialize the logger for this test module
log = Loggen.log_generator()


# This test should run first to check if the API is up before other tests
@pytest.mark.order(1)
@pytest.mark.e2e
@pytest.mark.api
# The test function uses a pytest fixture: api_context (for making API calls)
def test_get_status(api_context, data_dir):
    log.info("Starting test: test_get_status - Checking API health status.")
    # Make a GET request to the /status endpoint to check if the API is running and healthy
    log.info("Making GET request to /status endpoint.")
    response = api_context.get("/status")
    # Parse the JSON response to get the status information
    log.info("Parsing response from /status endpoint.")
    data = response.json()

    # Assert that the response is OK (HTTP 200)
    log.info("Asserting that the /status endpoint returned 200 OK.")
    assert response.ok, 'Status endpoint did not return 200 OK'
    # Assert that the status field in the response is "UP" (indicating the API is healthy)
    log.info("Asserting that the API status is UP.")
    assert data["status"] == "UP", f'Expected "UP" but got {data["status"]}'
    # Double-check that the response status code is 200
    log.info("Asserting that the response status code is 200.")
    assert response.status == 200, 'API response is not equal to 200.'

    # Save the cart details to a JSON file for potential debugging or reuse in other tests
    log.info("Saving API status response to a JSON file for debugging.")
    with open(data_dir / 'simple_grocery_store_status.json', 'w') as f:
        json.dump(data, f, indent=4)

    log.info("✓ Test completed successfully: API status is UP.")
