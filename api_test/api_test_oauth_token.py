import requests
import json
import datetime
from dotenv import load_dotenv
import os
load_dotenv('.env')


def generate_oauth_token_api():
    """
    This function generates an OAuth token by sending a POST request to a specified URL using the client ID and client secret provided as environment variables.
    
    Inputs:
    - None (the function uses environment variables to get the token URL, client ID, and client secret)
    
    Outputs:
    - If the OAuth token is generated successfully, the function returns a success message.
    - If the OAuth token cannot be generated, the function returns an error message.
    
    Additional aspects:
    - The function uses the 'requests' library to send HTTP requests.
    - The function uses the 'os' library to get environment variables.
    - The function uses a 'try-except' block to handle exceptions that may occur during the HTTP request.
    """
    url = os.environ['TOKEN_URL']
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "clientId": os.environ['VALID_CLIENT_ID'],
        "clientSecret": os.environ['VALID_CLIENT_SECRET']
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        access_token = response_json.get('accessToken')

        log_message = f"{generate_timestamp()} -(oAuth_Test) Test Result: Status Code {response.status_code}, Response JSON {response.json()}\n"
        with open(os.environ['PATH_TO_AUTH_LOGS'], 'a') as log_file:
            log_file.write(log_message)

        print("Token generated successfully")
        return access_token

    except requests.exceptions.RequestException as e:
        error_message = f"{generate_timestamp()} -(oAuth_Test) Error: {e} Status Code {response.status_code} \n"
        with open(os.environ['PATH_TO_AUTH_LOGS'], 'a') as log_file:
            log_file.write(error_message)

        print("Token could not be generated. Please refer to the oauth log file")
        return None


def generate_timestamp():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return timestamp


#def generate_valid_access_token():
    """
    Generates a valid access token by sending a POST request to the specified token URL with the client ID and client secret.
    This is then used throughout the api_test and py_test

    Returns:
    - Access token (str) if the request is successful.
    - None if there is an error with the request.
    """
    url = os.environ['TOKEN_URL']
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "clientId": os.environ['VALID_CLIENT_ID'],
        "clientSecret": os.environ['VALID_CLIENT_SECRET']
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        response_json = response.json()
        access_token = response_json.get('accessToken')

        return access_token

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None