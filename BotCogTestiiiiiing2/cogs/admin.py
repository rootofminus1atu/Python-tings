import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore
from errors import *



class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    # doesn't work here either
    @app_commands.command()
    @is_in_guild(1031977836849922108)
    async def inadmin(self, interaction: discord.Interaction):
        await interaction.response.send_message("lol check in admin")


async def setup(bot: commands.Bot):
    await bot.add_cog(admin(bot))
