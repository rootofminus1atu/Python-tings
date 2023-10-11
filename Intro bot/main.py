import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import os
import requests
from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"{bot.user} is now running!")

    # for syncing slash commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


# a regular command example
@bot.command()
async def hello(ctx: commands.Context):
    await ctx.send(f"Hello {ctx.author.global_name}")


# a slash command example
# BUT IT REQUIRES A COMMANDS SYNC
@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}!")


# more involved example
@bot.tree.command(name="say", description="I will say something for you")
@app_commands.describe(text="What should I say?")
@app_commands.describe(channel="Where should I say it?")
async def say(interaction: discord.Interaction, text: str, channel: discord.TextChannel):
    await channel.send(text)
    await interaction.response.send_message("The message was sent", ephemeral=True)


# api example
@bot.command()
async def cat(ctx: commands.Context):
    cat_response = requests.get("https://api.thecatapi.com/v1/images/search").json()
    cat_img = cat_response[0]['url']
    await ctx.send(cat_img)


bot.run(os.getenv('TOKEN'))
