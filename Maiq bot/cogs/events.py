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
        self.papiez.start()
        self.change_status.start()

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

    @tasks.loop(seconds=60)  # this command could be improved and be more accurate I think
    async def papiez(self):
        channel = self.bot.get_channel(papiez_channel_id)  # insert your channel id instead
        ie_date = datetime.now(pytz.timezone('Eire'))
        ie_time = ie_date.strftime('%H:%M')

        if ie_time == "21:37":
            await channel.send(
                "<a:papiez:1062048799947759626> 21:37 <a:papiez:1062048799947759626>")

    @tasks.loop(seconds=60)
    async def change_status(self):
        for activity in activity_list:
            typ, name = activity
            await self.bot.change_presence(activity=discord.Activity(type=typ, name=name))
            await asyncio.sleep(60)

async def setup(bot):
    await bot.add_cog(events(bot))
