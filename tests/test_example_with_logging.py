# """
# Example test showing how to integrate logging and markers with existing tests.
# This demonstrates the production-ready features without modifying core test logic.
# """
#
# import json
# import pytest
# import allure
#
#
# @pytest.mark.smoke
# @pytest.mark.critical
# @pytest.mark.auth
# @allure.epic("API Testing")
# @allure.feature("Authentication")
# @allure.story("Client Registration")
# @allure.severity(allure.severity_level.CRITICAL)
# def test_register_a_new_client_with_logging(api_context, data_dir, api_logger):
#     """
#     Enhanced version of client registration test with logging and Allure reporting.
#     This shows how to add logging without changing the core test logic.
#     """
#     from faker import Faker
#
#     # Create an instance of the Faker class to generate random client names and emails
#     fake = Faker()
#
#     # Prepare the payload with a unique client name and email for registration
#     client_details = {
#         "clientName": fake.name(),
#         "clientEmail": fake.email()
#     }
#
#     # Log the request
#     api_logger.log_request("POST", "/api-clients", data=client_details)
#
#     # Make a POST request to the /api-clients endpoint to register a new API client
#     response = api_context.post("/api-clients", data=client_details)
#
#     # Log the response
#     api_logger.log_response(response.status, response.json())
#
#     # Assert that the response status is 201 (Created) indicating successful registration
#     assert response.status == 201, f'Expected 201 Created but got {response.status}.'
#
#     # Parse the JSON response to extract the access token
#     access_token = response.json()
#
#     # Save the access token to a text file for potential debugging or reuse in other tests
#     with open(data_dir / 'simple_grocery_store_last_generated_access_token.json', 'w') as f:
#         json.dump(access_token, f, indent=4)
#
#     # Save the client details to a JSON file for potential debugging or reuse in other tests
#     with open(data_dir / 'simple_grocery_store_last_created_client_details.json', 'w') as f:
#         json.dump(client_details, f, indent=4)
#
#     # Assert that the access token is present in the response and is a non-empty string
#     assert access_token, 'Access token is missing in the response.'
#     assert isinstance(access_token, dict), f'Access token should be a dictionary. got {type(access_token)}.'
#
#     # Combine the client details and access token into a single dictionary for potential use in other tests
#     new_client = {
#         "client_name": client_details['clientName'],
#         "client_email": client_details['clientEmail'],
#         "access_token": access_token['accessToken']
#         # Assuming the access token is returned in a field named 'accessToken'
#     }
#
#     # Load existing client details from file, or create empty list if file doesn't exist
#     all_clients_file = data_dir / 'simple_grocery_store_all_client_details.json'
#     try:
#         with open(all_clients_file, 'r') as f:
#             all_client_details = json.load(f)
#         # Ensure it's a list
#         if not isinstance(all_client_details, list):
#             all_client_details = []
#     except (FileNotFoundError, json.JSONDecodeError):
#         # File doesn't exist or is empty/corrupted, start with empty list
#         all_client_details = []
#
#     # Append the new client to the list
#     all_client_details.append(new_client)
#
#     # Save the updated list back to the file
#     with open(all_clients_file, 'w') as f:
#         json.dump(all_client_details, f, indent=4)
#
#
# @pytest.mark.regression
# @pytest.mark.api
# @pytest.mark.order(after="test_register_a_new_client_with_logging")
# @allure.epic("API Testing")
# @allure.feature("Orders")
# @allure.story("Get All Orders")
# def test_get_all_orders_with_logging(api_context, data_dir, api_logger):
#     """
#     Enhanced version of get all orders test with logging and proper test dependencies.
#     """
#     # Read the last generated access token from a JSON file (created by test_register_a_new_api_client)
#     with open(data_dir / 'simple_grocery_store_last_generated_access_token.json', 'r') as f:
#         access_token = json.load(f)
#
#     headers = {"Authorization": f"Bearer {access_token['accessToken']}"}
#
#     # Log the request
#     api_logger.log_request("GET", "/orders", headers=headers)
#
#     # Make a GET request to retrieve all orders for the authenticated client
#     response = api_context.get("/orders", headers=headers)
#
#     # Log the response
#     api_logger.log_response(response.status, response.json())
#
#     # Assert that the response status is 200 (OK) indicating successful retrieval of orders
#     assert response.status == 200, f'Expected 200 OK but got {response.status}.'
#
#     # Parse the JSON response to get the list of orders
#     orders = response.json()
#
#     # Save the list of orders to a JSON file for potential debugging or reuse in other tests
#     with open(data_dir / 'simple_grocery_store_all_orders.json', 'w') as f:
#         json.dump(orders, f, indent=4)
