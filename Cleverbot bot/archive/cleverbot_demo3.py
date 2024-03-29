import requests
import hashlib
import re
import datetime

cookies = None
sessions = dict()

def get_date():
    return datetime.datetime.now().strftime("%Y%m%d")

def cleverbot(stimulus, context=[], session=None):
    global cookies, sessions
    if (cookies is None):
        req = requests.get("https://www.cleverbot.com/extras/conversation-social-min.js?{}".format(get_date()))
        cookies = {
            'XVIS': re.search(
                r"\w+(?=;)",
                req.headers["Set-cookie"]).group()}
    payload = f"stimulus={requests.utils.requote_uri(stimulus)}&"

    _context = context[:]
    reverseContext = list(reversed(_context))

    for i in range(len(_context)):
        payload += f"vText{i + 2}={requests.utils.requote_uri(reverseContext[i])}&"

    if session:
        # Creates new session if not exist
        if session not in sessions.keys():
            sessions[session] = list()

        _session = list(reversed(sessions[session]))
        # Adding the session to the payload
        for i in range(len(sessions[session])):
            payload += f"vText{i + len(_context) + 2}={requests.utils.requote_uri(_session[i])}&"

        # Adds the context to the session
        sessions[session] = _context + sessions[session]

    payload += "cb_settings_scripting=no&islearning=1&icognoid=wsf&icognocheck="

    payload += hashlib.md5(payload[7:33].encode()).hexdigest()

    print(payload)
    print(sessions)

    req = requests.post(
        "https://www.cleverbot.com/webservicemin?uc=UseOfficialCleverbotAPI",
        cookies=cookies,
        data=payload)
    getresponse = re.split(r'\\r',str(req.content))[0]
    print(getresponse)
    print(req.content)
    response = getresponse[2:-1]
    if session:
        sessions[session].extend([stimulus, response])
    return response


if __name__ == "__main__":
    # With context and session
    # An ongoing conversation with the first question as "How are you?"
    print("How are you?")
    print(cleverbot(input(">>"), session="cat"))
    while True:
        print(cleverbot(input(">>"), session="cat"))