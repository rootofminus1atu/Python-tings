import requests
import hashlib
import re
import datetime
from collections import deque
import aiohttp
import asyncio

class CleverbotConversation:
    def __init__(self, max_context: int = 100):
        self.cookies = None
        self.context_queue = deque(maxlen=max_context)
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
            print(self.cookies)

    def build_payload(self, stimulus: str):
        payload = f"stimulus={requests.utils.requote_uri(stimulus)}&"

        for i, context in enumerate(reversed(self.context_queue), start=2):
            payload += f"vText{i}={requests.utils.requote_uri(context)}&"

        payload += "cb_settings_scripting=no&islearning=1&icognoid=wsf&icognocheck="
        payload += hashlib.md5(payload[7:33].encode()).hexdigest()

        print(payload)
        return payload

    def send_cleverbot_request(self, payload: str):
        # works perfectly fine

        res = requests.post(
            "https://www.cleverbot.com/webservicemin?uc=UseOfficialCleverbotAPI",
            cookies=self.cookies,
            data=payload
        )

        get_response = re.split(r'\\r', str(res.content))[0]
        response = get_response[2:-1]
        return response
    
    async def send_cleverbot_request_async(self, payload: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://www.cleverbot.com/webservicemin?uc=UseOfficialCleverbotAPI",
                cookies=self.cookies,
                data=payload,
                allow_redirects=False
            ) as response:
                
                content = await response.text()
                # some possible further parsing here
                return content

    def respond(self, stimulus: str):
        payload = self.build_payload(stimulus)
        response = self.send_cleverbot_request(payload)
        self.context_queue.append(stimulus)
        self.context_queue.append(response)

        print(self.context_queue)

        return response
    
    async def respond_async(self, stimulus: str):
        payload = self.build_payload(stimulus)
        response = await self.send_cleverbot_request_async(payload)
        self.context_queue.append(stimulus)
        self.context_queue.append(response)

        return response
    
    def wipe_context(self):
        self.context_queue.clear()


async def main():
    # works perfectly fine
    conversation = CleverbotConversation()

    while True:
        user_input = input("You: ")
        response = conversation.respond(user_input)
        print(f"Bot: {response}")


async def main_async():
    # does NOT work
    conversation = CleverbotConversation()

    while True:
        user_input = input("You: ")
        response = await conversation.respond_async(user_input)
        print(f"Bot: {response}")


if __name__ == "__main__":
    asyncio.run(main_async())