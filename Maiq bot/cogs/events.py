import discord
from discord.ext import commands, tasks
from discord import app_commands
from colorama import Back, Fore, Style
import random
from datetime import datetime
import pytz
import asyncio
from files import *


class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.channel.id in art_channel_list:
            if message.embeds or message.attachments:
                await message.add_reaction('⭐')
                return

        if self.bot.user.mentioned_in(message):
            await message.reply(random.choice(maiq_quotes))
            return

    @tasks.loop(seconds=60)  # hello, this command could be improved and more accurate I think
    async def papiez(self):
        channel = self.bot.get_channel(1031977836849922111)  # insert your channel id instead
        ie_date = datetime.now(pytz.timezone('Ireland'))
        ie_time = ie_date.strftime('%H:%M')

        if ie_time == "21:37":
            await channel.send(
                "<a:papiez:1062048799947759626> 21:37 <a:papiez:1062048799947759626>")


async def setup(bot):
    await bot.add_cog(events(bot))
