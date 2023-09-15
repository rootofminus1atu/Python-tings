import discord
from discord.ext import commands
import asyncio
import requests
import time
import re
import os
import concurrent.futures
from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Create a ThreadPoolExecutor for running blocking functions
bot.executor = concurrent.futures.ThreadPoolExecutor()

# Your Chuck Norris API URL
CHUCK_NORRIS_API_URL = "https://api.chucknorris.io/jokes/random"


def blocking_io(sleep_duration: int):
    print(f"start blocking_io at {time.strftime('%H:%M:%S')}")

    response = requests.get(CHUCK_NORRIS_API_URL)
    joke = response.json()['value']

    print(f"Sleeping for {sleep_duration} second(s)")
    time.sleep(sleep_duration)  
    print(f"ended blocking_io at {time.strftime('%H:%M:%S')}")
    
    return joke


@bot.command()
async def chuck(ctx, sleep_duration: int):
    await ctx.send("Fetching a Chuck Norris joke...")
    
    joke = await bot.loop.run_in_executor(bot.executor, blocking_io, sleep_duration)
    # OR just use asyncio.to_thread
    # joke = await asyncio.to_thread(blocking_io, sleep_duration)

    await ctx.send(f"Chuck Norris joke: {joke}")



@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


bot.run(os.getenv('TOKEN'))