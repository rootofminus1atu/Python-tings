import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore
import inflect
p = inflect.engine()



class testing_grounds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    # music here!




async def setup(bot):
    await bot.add_cog(testing_grounds(bot))
