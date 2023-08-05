import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore

class CogBase(commands.Cog):
    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog ready!")

    async def cog_load(self) -> None:
        print(Fore.GREEN + self.__class__.__name__ + Fore.RESET + " cog loaded")

    async def cog_unload(self) -> None:
        print(Fore.GREEN + self.__class__.__name__ + Fore.RESET + " cog unloaded")

async def setup(bot):
    print("Loading CogBase")