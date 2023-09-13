import asyncio
import cleverbotfree
"""
def chat():
    # Example code using cleverbotfree sync api.
    with cleverbotfree.sync_playwright() as p_w:
        c_b = cleverbotfree.Cleverbot(p_w)
        while True:
            user_input = input("User: ")
            if user_input == 'quit':
                break
            bot = c_b.single_exchange(user_input)
            print('Cleverbot:', bot)
        c_b.close()

chat()

async def async_chat():
    # Example code using cleverbotfree async api.
    async with cleverbotfree.async_playwright() as p_w:
        c_b = await cleverbotfree.CleverbotAsync(p_w)
        while True:
            user_input = input("User: ")
            if user_input == 'quit':
                break
            bot = await c_b.single_exchange(user_input)
            print('Cleverbot:', bot)
        await c_b.close()

asyncio.run(async_chat())
"""

import time

start_time = time.time()

async def gcr(msg: str) -> str:
    rn = time.time() - start_time
    print("gonna enter the async with pw", rn)
    async with cleverbotfree.async_playwright() as pw:
        rn = time.time() - start_time
        print("Entered async with pw", rn)
        cb = await cleverbotfree.CleverbotAsync(pw)
        rn = time.time() - start_time
        print("got cb", rn)
        response = await cb.single_exchange(msg)
        rn = time.time() - start_time
        print("got response", rn)
        await cb.close()
        rn = time.time() - start_time
        print("closed cb", rn)
        return response
    return "oops, something went wrong"



async def get_cleverbot_response(msg: str) -> str:
    rn = time.time() - start_time
    print("gonna enter the async with pw", rn)
    async with cleverbotfree.async_playwright() as p_w:
        rn = time.time() - start_time
        print("gonna enter the async with cb", rn)
        async with cleverbotfree.CleverbotAsync(p_w) as c_b:
            rn = time.time() - start_time
            print("entered", rn)
            response = await c_b.single_exchange(msg)
            rn = time.time() - start_time
            print("got response", rn)
            return response

# example scenario:
async def main():
    msg = "who are you then"
    response = await get_cleverbot_response(msg)
    print(response)
    rn = time.time() - start_time
    print("finishing", rn)

asyncio.run(main())