import asyncio

async def main():
    task = asyncio.create_task(other_func())
    print("A")
    await asyncio.sleep(2)
    print("B")
    return_value = await task
    print(f"Return value is {return_value}")


async def other_func():
    print("1")
    await asyncio.sleep(5)
    print("2")
    return 10

asyncio.run(main())
