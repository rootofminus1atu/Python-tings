import requests
import hashlib
import re
import datetime

class CleverbotConversation:
    def __init__(self):
        self.cookies = None
        self.sessions = {}
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

    def build_payload(self, stimulus, context=[], session=None):
        payload = f"stimulus={requests.utils.requote_uri(stimulus)}&"

        _context = context[:]
        reverse_context = list(reversed(_context))

        for i in range(len(_context)):
            payload += f"vText{i + 2}={requests.utils.requote_uri(reverse_context[i])}&"

        if session:
            if session not in self.sessions.keys():
                self.sessions[session] = []

            _session = list(reversed(self.sessions[session]))
            for i in range(len(self.sessions[session])):
                payload += f"vText{i + len(_context) + 2}={requests.utils.requote_uri(_session[i])}&"

            self.sessions[session] = _context + self.sessions[session]

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

    def cleverbot(self, stimulus, context=[], session=None):
        payload = self.build_payload(stimulus, context, session)
        return self.send_cleverbot_request(payload)

    def start_conversation(self):
        print("How are you?")
        initial_question = "How are you?"
        context = ["hi.", initial_question]

        while True:
            user_input = input(">> ")
            response = self.cleverbot(user_input, context, initial_question)
            print(response)

if __name__ == "__main__":
    conversation = CleverbotConversation()
    conversation.start_conversation()
