import discord
from discord.ext import commands, tasks
from discord import app_commands
from colorama import Back, Fore, Style
import random
from datetime import datetime, time
import asyncio


class reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminding.start()
        self.LOOPTESTING.start()


    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    def cog_unload(self):
        self.reminding.cancel()
        self.LOOPTESTING.cancel()

    @tasks.loop(seconds=1)
    async def LOOPTESTING(self):
        # channel = self.bot.get_channel(1031977836849922111)
        print(f"Time rn: {datetime.now().time()}")

    full_hours = [time(hour=hour, minute=0) for hour in range(24)]

    @tasks.loop(time=self.full_hours)
    async def reminding(self):
        asyncio.sleep(1)  # sleep for 1 sec because discord updates hours too slowly for this
        print(self.full_hours)
        channel = self.bot.get_channel(1031977836849922111)
        print(datetime.now().time())
        await channel.send("FULL HOUR TEST")

    """
    @hourly_task.before_loop
    async def wait_until_7am():
        # this will use the machine's timezone
        # to use a specific timezone use `.now(timezone)` without `.astimezone()`
        # timezones can be acquired using any of
        # `datetime.timezone.utc`
        # `datetime.timezone(offset_timedelta)`
        # `pytz.timezone(name)` (third-party package)
        now = datetime.datetime.now().astimezone()
        next_run = now.replace(hour=7, minute=0, second=0)

        if next_run < now:
            next_run += datetime.timedelta(days=1)

        await discord.utils.sleep_until(next_run)
    """

    @reminding.before_loop
    async def before_reminding(self):
        await self.bot.wait_until_ready()

    @LOOPTESTING.before_loop
    async def before_LOOPTESTING(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(reminder(bot))