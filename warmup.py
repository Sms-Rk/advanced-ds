import requests
import time

# Define the OpenFaaS gateway URL and the target function name
gateway_url = "http://gateway.openfaas:8080"
function_name = "mongodb-github"

# Define the payload for the function invocation
payload = {
    "key1": "value1",
    "key2": "value2"
}

# Function invoker loop
while True:
    try:
        # Make an HTTP POST request to the OpenFaaS gateway to invoke the function
        response = requests.post(f"{gateway_url}/function/{function_name}", json=payload)

        # Handle the response
        if response.status_code == 200:
            print("Function invocation successful")
        else:
            print(f"Function invocation failed with status code: {response.status_code}")

        # Wait for a specific interval before invoking the function again
        time.sleep(300)  # Adjust the interval as needed
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while invoking the function: {str(e)}")
        time.sleep(60)  # Wait for a shorter interval before retrying
