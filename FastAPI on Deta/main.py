from fastapi import FastAPI, Request
import requests
import hashlib
import re
import asyncio

app = FastAPI()

@app.get("/")
async def root():
    return "come forth"

@app.post("/api/clevreq")
async def clevreq(request: Request):
    json_data = await request.json()

    return {"got_json": json_data}
