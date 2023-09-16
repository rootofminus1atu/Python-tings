import requests
import hashlib
import re
import argparse

class CleverbotError(Exception):
    pass

def post_to_cleverbot(cookie, payload):
    try:
        # Calculate MD5 hash
        payload_with_hash = payload + hashlib.md5(payload[7:33].encode()).hexdigest()

        # Send the POST request
        response = requests.post(
            "https://www.cleverbot.com/webservicemin?uc=UseOfficialCleverbotAPI",
            cookies={'XVIS': cookie},
            data=payload_with_hash
        )

        response.raise_for_status()  # Raise an exception if the request fails

        # Extract and format the response
        cleverbot_text = re.split(r'\\r', str(response.content))[0]
        output = cleverbot_text[2:-1]

        return output

    except requests.exceptions.RequestException as e:
        raise CleverbotError(f"HTTP Request Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Cleverbot Program')
    parser.add_argument('--cookie', type=str, required=True, help='The cookie string from XVIS')
    parser.add_argument('--payload', type=str, required=True, help='The payload string including the stimulus and queue, already built to be sent to the API')

    args = parser.parse_args()
    cookie = args.cookie
    payload = args.payload

    try:
        output = post_to_cleverbot(cookie, payload)
        print(output)
    except CleverbotError as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()







