import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from colorama import Fore
from typing import Optional

class helpers():
    def __init__(self, bot):
        self.bot = bot

    async def get_or_fetch_user(self, user_id: int) -> Optional[discord.User]:
        try:
            return self.get_user(user_id) or await self.fetch_user(user_id)
        except discord.NotFound:
            return None

    def print_report(text):
        rn = datetime.now().strftime("%y-%m-%d %H:%M:%S")
        print(f"{Fore.LIGHTBLACK_EX}[{rn}]{Fore.RESET} {text}")

async def setup(bot):
    bot.helpers = helpers(bot)