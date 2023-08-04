import discord
from discord.ext import commands, tasks
from discord import app_commands
from colorama import Back, Fore, Style
import random
from datetime import datetime, time
import asyncio
import pytz
from zoneinfo import ZoneInfo
import tzdata

# some_hour_might_be_important_later = time(hour=22, minute=53, tzinfo=ZoneInfo('Europe/Warsaw'))


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

    @tasks.loop(seconds=100)
    async def LOOPTESTING(self):
        print(f"Time rn: {datetime.now().time()}")
        print(f"Time utc rn: {datetime.utcnow().time()}")

    full_hours = [time(hour=hour, minute=10) for hour in range(24)]

    @tasks.loop(time=full_hours)
    async def reminding(self):
        print("=====================================")
        start = datetime.utcnow()
        print(start)

        now = datetime.utcnow()

        result = self.bot.manager.get_configs_with_birthdays_for_datetime(now)

        for config in result:
            embed = discord.Embed(
                title="🎉 Birthdays today! 🎉",
                description="\n".join([f"{birthday['person']} - {birthday['day']}/{birthday['month']}" for birthday in config["birthdays"]]),
                color=discord.Color.random())
            embed.set_footer(
                text=now.strftime("%d/%m/%Y %H:%M UTC"))

            if "channel_id" in config:
                channel = self.bot.get_channel(config["channel_id"])
                await channel.send(embed=embed)
            else:
                user = await self.bot.get_or_fetch_user(config["user_id"])
                await user.send(embed=embed) 

        end = datetime.utcnow()
        print(end)
        print(f"Time elapsed: {end - start}")
        print("=====================================")

    @commands.command(name="loopinvoke")
    async def loopinvoke(self, ctx):
        now = datetime.utcnow().replace(minute=0, hour=8, day=24, month=1)
        print(now)

        result = self.bot.manager.get_configs_with_birthdays_for_datetime(now)
        print(result)

        embed = discord.Embed(
            title="🎉 Birthdays today! 🎉", 
            description=str(result),
            color=discord.Color.random())
        embed.set_footer(
            text=now.strftime("%d/%m/%Y %H:%M UTC"))
        
        await ctx.send(embed=embed)



    @commands.command(name="test")
    async def test(self, ctx, hour: int):
        # for now only Europe/Warsaw
        self.bot.testing.create_time(hour, "Europe/Warsaw")
        await ctx.send("test")

    @commands.command(name="hour")
    async def hour(self, ctx):
        print("hi")
        another = time(hour=22, minute=50, tzinfo=ZoneInfo('Europe/Warsaw'))
        print(another)
        print(another.tzinfo)
        await ctx.send(f"Time rn: {datetime.now()} vs utc {datetime.utcnow()} vs pytz utc {datetime.now(pytz.utc)}")

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