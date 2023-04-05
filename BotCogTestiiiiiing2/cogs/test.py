import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore

from errors import *

# the cog whose purpose is to handle errors






# the cog with commands
class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    # but it works just fine from here
    @app_commands.command()
    @lol_check(1072254384613888020)
    async def intest(self, interaction: discord.Interaction):
        await interaction.response.send_message("all good because it's in the same file")


async def setup(bot: commands.Bot):
    await bot.add_cog(test(bot))
