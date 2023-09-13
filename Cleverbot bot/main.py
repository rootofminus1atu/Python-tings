import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
load_dotenv()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(os.getenv('TOKEN'))