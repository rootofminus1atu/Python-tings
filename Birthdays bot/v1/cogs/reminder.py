import discord
from discord.ext import commands, tasks
from discord import app_commands
from colorama import Back, Fore, Style
import random
from datetime import datetime
import asyncio
from managers import birthdays_manager


class reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = birthdays_manager(bot)
        self.reminding.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    def cog_unload(self):
        self.reminding.cancel()

    @tasks.loop(hours=1)
    async def reminding(self):
        # each hour check if any servers/users want to be reminded then
        # aka get all configs where time is now
        configs = self.manager.find_birthdays_for_time(datetime.now().hour)
        print(datetime.now().hour)
        print(configs)

        # for each config server/user:
            # check if any birthdays are today
            # if so, send message to channel/dm
        for config in configs:
            if config['server_id']:
                server = self.bot.get_guild(config['server_id'])
                channel = server.get_channel(config['channel_id'])
                await channel.send("test")
            else:
                user = await self.bot.get_or_fetch_user(config['dm_id'])
                await user.send("test")

        # in case of delays

        # =================================================================
        # or
        # get all configs which want to be reminded at this hour
        # get all birthdays for today

        # for each config server/user:
            # send a list with 

        pass


    @reminding.before_loop
    async def before_reminding(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(reminder(bot))