import aiohttp
import asyncio
import re
import requests
import datetime

class YourCleverbotClient:
    def __init__(self):
        self.cookies = None
        self.initialize_cookies()

    def get_date(self):
        return datetime.datetime.now().strftime("%Y%m%d")

    def initialize_cookies(self):
        if self.cookies is None:
            req = requests.get("https://www.cleverbot.com/extras/conversation-social-min.js?{}".format(self.get_date()))
            self.cookies = {
                'XVIS': re.search(
                    r"\w+(?=;)",
                    req.headers["Set-cookie"]).group()
            }

    async def send_cleverbot_request(self, payload):
        url = 'https://www.cleverbot.com/webservicemin?uc=UseOfficialCleverbotAPI'

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, cookies=self.cookies) as response:
                if response.status == 200:
                    content = await response.text()
                    get_response = re.split(r'\\r', content)[0]
                    response = get_response[2:-1]

                    # Check if the server set any new cookies in the response
                    set_cookie_header = response.headers.get('Set-Cookie')
                    if set_cookie_header:
                        print(f"Server set the following new cookie: {set_cookie_header}")
                    else:
                        print("No new cookies set by the server")

                    return response
                else:
                    return None

async def main():
    client = YourCleverbotClient()
    payload = "YourPayloadHere"  # Replace with your payload

    response = await client.send_cleverbot_request(payload)

    if response:
        print(f"Cleverbot response: {response}")
    else:
        print("Request failed")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
