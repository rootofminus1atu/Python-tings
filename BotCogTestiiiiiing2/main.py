import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
from errors import *
from dotenv import load_dotenv
load_dotenv()


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), tree_cls=TreeWithErrors)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


async def load_cogs():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')


# default check and default error type
# works from here (and from other cogs)
@app_commands.checks.cooldown(1, 30)
@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong!")

# custom check and custom error type
# doesn't work here
@bot.tree.command(name="inmain")
@lol_check(1061385736642908210)
async def inmain(interaction: discord.Interaction):
    await interaction.response.send_message("lol check in main")



asyncio.run(load_cogs())
bot.run(os.getenv('bot_key'))
