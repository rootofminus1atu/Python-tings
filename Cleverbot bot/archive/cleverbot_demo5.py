import requests
import hashlib
import re
import datetime
import aiohttp

# TODO:
# oop-ify
# async-ify

class Cleverbot:
    def __init__(self):
        self.cookies = None  # ig the cookie could be stored in a db or something  # but its fine being regenerated like that
        self.sessions = {}
        self.initialize_cookies()

    def get_date(self):
        return datetime.datetime.now().strftime("%Y%m%d")

    def initialize_cookies(self):
        if self.cookies is None:
            req = requests.get("https://www.cleverbot.com/extras/conversation-social-min.js?{}".format(self.get_date()))
            print(req.headers)
            self.cookies = {
                'XVIS': re.search(
                    r"\w+(?=;)",
                    req.headers["Set-cookie"]).group()
            }

    def requests_requote(self, url):
        return requests.utils.requote_uri(url)
    
    def aiohttp_requote(self, url):
        return aiohttp.helpers.requote_uri(url)
    
    def build_payload(self, stimulus, context=None):
        payload = f"stimulus={self.requests_requote(stimulus)}&"

        if context:
            _context = list(context)
            reverse_context = list(reversed(_context))
            
            for i in range(len(_context)):
                payload += f"vText{i + 2}={self.requests_requote(reverse_context[i])}&"

        payload += "cb_settings_scripting=no&islearning=1&icognoid=wsf&icognocheck="
        payload += hashlib.md5(payload[7:33].encode()).hexdigest()

        return payload

if __name__ == "__main__":
    input_string = "Hello, world!"
    url_encoded_string = requests.utils.requote_uri(input_string)

    print(url_encoded_string)
