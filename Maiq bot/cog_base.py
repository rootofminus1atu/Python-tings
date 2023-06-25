import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore

class CogBase():
    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.GREEN + self.__class__.__name__ + Fore.RESET + " cog loaded")