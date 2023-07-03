import discord
from discord.ext import commands
from discord.ui import Select, View
from discord import app_commands
from colorama import Fore
import gspread
import inflect
p = inflect.engine()



class testing_grounds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    @app_commands.command(name="hi", description="Hi!")
    async def hi(self, interaction: discord.Interaction):
        self.bot.db_manager.say_hi()

        await interaction.response.send_message("hi!")


async def setup(bot):
    await bot.add_cog(testing_grounds(bot))
