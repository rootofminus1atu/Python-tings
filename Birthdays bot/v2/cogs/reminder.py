import discord
from discord.ext import commands, tasks
from discord import app_commands
from colorama import Back, Fore, Style
import random
from datetime import datetime
import asyncio


class reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminding.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    def cog_unload(self):
        self.reminding.cancel()

    @tasks.loop(minutes=1)
    async def reminding(self):
        channel = self.bot.get_channel(1031977836849922111)
        await channel.send("Hello there is a birthday today!")


    @reminding.before_loop
    async def before_reminding(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(reminder(bot))