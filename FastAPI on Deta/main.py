from fastapi import FastAPI, Request
import requests
import hashlib
import re
import asyncio
from typing import List

app = FastAPI()

@app.get("/")
async def root():
    return "come forth"

@app.get("/about")
async def about():
    return "about"


@app.post("/api/test")
async def test(request: Request):
    json_data = await request.json()
    return {"the_json_data": json_data}



def construct_payload(stimulus: str, context: List[str]):
    payload = f"stimulus={requests.utils.requote_uri(stimulus)}&"

    # notice that the queue is reversed
    for i, msg in enumerate(reversed(context), start=2):
        payload += f"vText{i}={requests.utils.requote_uri(msg)}&"

    payload += "cb_settings_scripting=no&islearning=1&icognoid=wsf&icognocheck="
    payload += hashlib.md5(payload[7:33].encode()).hexdigest()
    
    return payload

def get_cleverbot_response(payload: str, cookie: str):
    key, val = cookie.split('=')
    cookie_dict = {key: val}

    response = requests.post(
        "https://www.cleverbot.com/webservicemin?uc=UseOfficialCleverbotAPI",
        cookies=cookie_dict,
        data=payload
    )

    text = re.split(r'\\r', str(response.content))[0]
    text_cleared = text[2:-1]

    return text_cleared

@app.post("/api/clevreq")
async def clevreq(request: Request):
    api_key = request.headers.get('clevreq-api-key')
    cookie = request.headers.get('cookie')
    # verify key something something

    json_data = await request.json()

    stimulus = json_data.get('stimulus')
    context = json_data.get('context')
    # === above belongs to special parsing method ===
    # one day in the future

    payload = construct_payload(stimulus, context)
    response = await asyncio.to_thread(get_cleverbot_response, payload, cookie)

    print(f"Response is: ({response})")

    return response