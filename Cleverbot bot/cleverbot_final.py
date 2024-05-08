import requests
import hashlib
import re
import datetime
from collections import deque

class CleverbotConversation:
    def __init__(self, max_context=100):
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

    def build_payload(self, stimulus):
        payload = f"stimulus={requests.utils.requote_uri(stimulus)}&"

        # notice that the queue is reversed
        for i, context in enumerate(reversed(self.context_queue), start=2):
            payload += f"vText{i}={requests.utils.requote_uri(context)}&"

        payload += "cb_settings_scripting=no&islearning=1&icognoid=wsf&icognocheck="
        payload += hashlib.md5(payload[7:33].encode()).hexdigest()

        return payload

    def send_cleverbot_request(self, payload):
        req = requests.post(
            "https://www.cleverbot.com/webservicemin?uc=UseOfficialCleverbotAPI",
            cookies=self.cookies,
            data=payload
        )
        get_response = re.split(r'\\r', str(req.content))[0]
        response = get_response[2:-1]
        return response

    def respond(self, stimulus):
        payload = self.build_payload(stimulus)
        response = self.send_cleverbot_request(payload)
        self.context_queue.append(stimulus)
        self.context_queue.append(response)

        return response
    
    def wipe_context(self):
        self.context_queue.clear()

    def start_conversation(self):
        print("Your conversation with Cleverbot has started.")
        while True:
            user_input = input("You: ")
            response = self.respond(user_input)
            print(f"Bot: {response}")

if __name__ == "__main__":
    conversation = CleverbotConversation()
    conversation.start_conversation()