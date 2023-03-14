import time
import asyncio

async def do_a1():
    print("a1 started")
    await asyncio.sleep(5)
    print("a1 finished")


async def do_a2():
    print("a2 started")
    await asyncio.sleep(7)
    print("a2 finished")
