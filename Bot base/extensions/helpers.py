import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from colorama import Fore

class helpers():
    def __init__(self, bot):
        self.bot = bot

    def print_report(text):
        rn = datetime.now().strftime("%y-%m-%d %H:%M:%S")
        print(f"{Fore.LIGHTBLACK_EX}[{rn}]{Fore.RESET} {text}")

async def setup(bot):
    bot.helpers = helpers(bot)