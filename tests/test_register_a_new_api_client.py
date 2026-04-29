"""
API: Register a New API Client
Endpoint: POST /api-clients

Description:
This API is used to register a new API client and generate an access token.
The request must be sent in JSON format.

Request Body Parameters:
- clientName (string) [Required]
  Name of the API client to be registered.

- clientEmail (string) [Required]
  Email address of the API client.
  NOTE: The email does NOT need to be real and will NOT be stored on the server.

Example Request Body:
{
    "clientName": "some name",
    "clientEmail": "example@gmail.com"
}

Response:
- 201 Created
  Client successfully registered.
  Response body will contain the generated access token.

- 400 Bad Request
  Returned when required parameters are missing or invalid.

- 409 Conflict
  Returned when a client has already been registered using the same email address.

Authentication:
No authentication is required for registering a new API client.
This endpoint is typically used to generate an access token for future API calls.
"""
# Importing Faker for generating random client names and emails, Loggen for logging, json for handling JSON data, and pytest for the test framework
from faker import Faker
from utilities.logger import Loggen
import json, pytest

# Initialize the logger for this test module
log = Loggen.log_generator()


@pytest.mark.order(7)
@pytest.mark.e2e
@pytest.mark.slow  # This test may take longer due to reading files and making API calls
# The test function uses pytest fixtures: api_context (for making API calls) and data_dir (for test data file paths)
def test_register_a_new_client(api_context, data_dir):
    log.info("Starting test: test_register_a_new_client - Registering a new API client and generating access token.")

    # Create an instance of the Faker class to generate random client names and emails
    fake = Faker()

    # Prepare the payload with a unique client name and email for registration
    log.info("Generating random client credentials using Faker.")
    client_details = {
        "clientName": fake.name(),
        "clientEmail": fake.email()
    }
    log.debug(f"Generated client name: {client_details['clientName']}, email: {client_details['clientEmail']}")

    # Make a POST request to the /api-clients endpoint to register a new API client
    log.info("Making POST request to /api-clients endpoint to register new client.")
    response = api_context.post("/api-clients", data=client_details)

    # Assert that the response status is 201 (Created) indicating successful registration
    log.info("Asserting that the /api-clients endpoint returned 201 Created.")
    assert response.status == 201, f'Expected 201 Created but got {response.status}.'

    # Parse the JSON response to extract the access token
    log.info("Parsing response to extract access token.")
    access_token = response.json()

    # Save the access token to a text file for potential debugging or reuse in other tests
    log.info("Saving access token to file for reuse in other tests.")
    with open(data_dir / 'simple_grocery_store_last_generated_access_token.json', 'w') as f:
        json.dump(access_token, f, indent=4)

    # Save the client details to a JSON file for potential debugging or reuse in other tests
    log.info("Saving client details to file for debugging and reuse.")
    with open(data_dir / 'simple_grocery_store_last_created_client_details.json', 'w') as f:
        json.dump(client_details, f, indent=4)

    # Assert that the access token is present in the response and is a non-empty string
    log.info("Asserting that access token is present in response.")
    assert access_token, 'Access token is missing in the response.'
    log.info("Asserting that access token is a dictionary.")
    assert isinstance(access_token, dict), f'Access token should be a dictionary. got {type(access_token)}.'

    # Combine the client details and access token into a single dictionary for potential use in other tests
    log.info("Combining client details and access token into single dictionary.")
    new_client = {
        "client_name": client_details['clientName'],
        "client_email": client_details['clientEmail'],
        "access_token": access_token['accessToken']
        # Assuming the access token is returned in a field named 'accessToken'
    }

    # Load existing client details from file, or create empty list if file doesn't exist
    log.info("Loading existing client details from file.")
    all_clients_file = data_dir / 'simple_grocery_store_all_client_details.json'
    try:
        with open(all_clients_file, 'r') as f:
            all_client_details = json.load(f)
        # Ensure it's a list
        if not isinstance(all_client_details, list):
            all_client_details = []
            log.debug("Client details file was not a list, initializing as empty list.")
    except (FileNotFoundError, json.JSONDecodeError):
        # File doesn't exist or is empty/corrupted, start with empty list
        log.debug("Client details file not found or corrupted, starting with empty list.")
        all_client_details = []

    # Append the new client to the list
    log.info("Appending new client to existing client details.")
    all_client_details.append(new_client)

    # Save the updated list back to the file
    log.info("Saving updated client details to file.")
    with open(all_clients_file, 'w') as f:
        json.dump(all_client_details, f, indent=4)

    log.info("✓ Test completed successfully: New API client registered and access token generated.")
