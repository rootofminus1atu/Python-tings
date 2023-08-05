import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore

class CogBase(commands.Cog):
    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog ready!")

    # cog load

    # cog unload

    # or something else

async def setup(bot):
    pass