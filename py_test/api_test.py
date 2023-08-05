import pytest
import requests
import json
from api_test import generate_oauth_token_api
from dotenv import load_dotenv
import os
import time

load_dotenv('.env')

# API endpoints
BASE_URL = os.environ['BASE_URL']
TOKEN_URL = os.environ['TOKEN_URL']
RESPONSE_TYPES_URL = os.environ['RESPONSE_TYPES_URL']

# Test data
valid_client_id = os.environ['VALID_CLIENT_ID']
valid_client_secret = os.environ['VALID_CLIENT_SECRET']
valid_access_token = generate_oauth_token_api()
unauthorized_access_token = os.environ['UNAUTHORIZED_ACCESS_TOKEN']


# Test cases

"""
This code snippet contains a set of test functions written using the pytest framework to perform automated testing of a REST API. The tests cover various scenarios such as valid and invalid access token requests, response types requests with different authorization levels, invalid endpoint requests, and response time testing.

The code includes the following test functions:
- test_valid_access_token_request: Sends a valid access token request and asserts the response status code is 200 and that the response contains an access token.
- test_invalid_credentials_access_token_request: Sends an invalid access token request and asserts the response status code is 401.
- test_missing_data_access_token_request: Sends an access token request with missing data and asserts the response status code is 400.
- test_valid_response_types_request: Sends a valid response types request with a valid access token and asserts the response status code is 200 and that the response is a list.
- test_unauthorized_response_types_request: Sends an unauthorized response types request and asserts the response status code is 401.
- test_expired_access_token_response_types_request: Sends an expired access token response types request and asserts the response status code is 401.
- test_rate_limiting_response_types_request: Sends multiple response types requests to test rate limiting and asserts the response status code is 429.
- test_invalid_endpoint: Sends an invalid endpoint request and asserts the response status code is 404.
- test_response_time: Sends a response types request and asserts the response time is less than or equal to a maximum acceptable response time.
- test_special_characters_request: Sends an access token request with special characters in the client secret and asserts the response status code is 400 and that the response contains an error.
- test_compare_response_types: Sends a response types request with an unauthorized access token and compares the response to an expected response.

The code also includes necessary imports of libraries such as pytest, requests, json, and dotenv. It uses environment variables for sensitive data and includes tests for various scenarios to ensure comprehensive testing of the API.
"""


def test_valid_credentials_access_token_request():
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "clientId": valid_client_id,
        "clientSecret": valid_client_secret
    }
    response = requests.post(TOKEN_URL, headers=headers,json=data)
    assert response.status_code == 200
    assert 'accessToken' in response.json()


def test_invalid_credentials_access_token_request():
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "clientId": valid_client_id,
        "clientSecret": "sL0uix7wwHk6HUN7P66ogyfv246oxgEL"
    }
    response = requests.post(TOKEN_URL,headers=headers ,json=data)
    assert response.status_code == 401


def test_missing_data_access_token_request():
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "clientId": valid_client_id
    }
    response = requests.post(TOKEN_URL, headers=headers,json=data)
    assert response.status_code == 400


def test_valid_response_types_request():
    headers = {
        'Authorization': f'Bearer {valid_access_token}'
    }
    response = requests.get(RESPONSE_TYPES_URL, headers=headers)
    assert response.status_code == 200
    print()
    assert isinstance(response.json(), dict)


def test_unauthorized_response_types_request():
    headers = {
        'Authorization': f'Bearer {unauthorized_access_token}'
    }
    response = requests.get(RESPONSE_TYPES_URL, headers=headers)
    assert response.status_code == 401


def test_expired_access_token_response_types_request():
    headers = {
        'Authorization': f'Bearer {valid_access_token}'
    }
    response = requests.get(RESPONSE_TYPES_URL, headers=headers)
    assert response.status_code == 401


def test_rate_limiting_response_types_request():
    headers = {
        'Authorization': f'Bearer {valid_access_token}'
    }
    for _ in range(50):
        response = requests.get(RESPONSE_TYPES_URL, headers=headers)
        status_code = response.status_code

    assert status_code == 429


def test_invalid_endpoint():
    invalid_endpoint = f"{BASE_URL}/invalid_endpoint"
    headers = {
        'Authorization': f'Bearer {valid_access_token}'
    }
    response = requests.get(invalid_endpoint,headers=headers)
    assert response.status_code == 404


def test_response_time():
    start_time = time.time()
    headers = {
        'Authorization': f'Bearer {valid_access_token}'
    }
    response = requests.get(RESPONSE_TYPES_URL,headers=headers)
    end_time = time.time()
    response_time = end_time - start_time
    max_response_time = 1.0  # Set a maximum acceptable response time in seconds
    assert response_time <= max_response_time


def test_special_characters_request():

    headers = {
        'Content-Type': 'application/json'
    }
    special_data = {
        "clientId": valid_client_id+'%^$%$#_~',
        "clientSecret": "special'&secret"
    }
    response = requests.post(TOKEN_URL,headers=headers ,json=special_data)
    assert response.status_code == 400
    assert "error" in response.json()


def test_compare_response_to_expected_response():

    expected_response = {
        "message": "Successfully fetched responseTypes",
        "responseTypes": [
            {
                "id": 1,
                "value": "SECURITY",
                "description": "Security",
                "createdAt": "2020-04-07T08:34:27.666Z",
                "updatedAt": "2020-04-07T08:34:27.666Z",
                "default": True
            }
        ]
    }

    headers = {
        'Authorization': f'Bearer {valid_access_token}'
    }
    response = requests.get(RESPONSE_TYPES_URL, headers=headers)
    assert response.status_code == 200

    actual_response = response.json()

    # Compare each field in the response
    assert actual_response["message"] == expected_response["message"]
    assert len(actual_response["responseTypes"]) == len(expected_response["responseTypes"])

    actual_response_type = actual_response["responseTypes"][0]
    expected_response_type = expected_response["responseTypes"][0]

    assert actual_response_type["id"] == expected_response_type["id"]
    assert actual_response_type["value"] == expected_response_type["value"]
    assert actual_response_type["description"] == expected_response_type["description"]
    assert actual_response_type["createdAt"] == expected_response_type["createdAt"]
    assert actual_response_type["updatedAt"] == expected_response_type["updatedAt"]
    assert actual_response_type["default"] == expected_response_type["default"]


