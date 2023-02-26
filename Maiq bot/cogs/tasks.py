import discord
from discord.ext import commands, tasks
from discord import app_commands
from colorama import Back, Fore, Style

# to-do:
# make tasks work cuz this doesn't work lol
# they work if they're in main, but not here for some reason


class tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hi.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    @tasks.loop(seconds=5)  # hello, this command could be improved and more accurate I think
    async def hi(self):
        channel = self.bot.get_channel(1031977836849922111)  # insert your channel id instead
        print("hi")
        await channel.send("hi")


async def setup(bot):
    await bot.add_cog(tasks(bot))
