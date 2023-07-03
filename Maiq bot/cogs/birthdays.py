import discord
from discord.ext import commands, tasks
from discord.ui import Select, View
from discord import app_commands
from colorama import Fore
from datetime import datetime
import pytz

from helpers import pretty_day_month

class birthdays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")
        self.bday_reminder.start()

    @app_commands.command(name="addbday", description="Add a birthday that Mai'q will remind you about!")
    @app_commands.describe(person="Whose birthday?", day="Which day?", month="Which month?")
    async def addbday(self, interaction: discord.Interaction, person: str, day: int, month: int):
        try:
            datetime(year=2023, month=month, day=day)
        except ValueError:
            await interaction.response.send_message(f"{day}/{month} is not a date in Mai'q's calendar.")
            return

        server = interaction.guild

        if not server:
            return await interaction.response.send_message("Mai'q will not listen to you in dms. (Maybe in the future)")
            
        self.bot.db_manager.add_birthday(server.id, person, day, month)

        await interaction.response.send_message(f"Mai'q will now remember that {person}'s birthday is on {day}/{month}.")
        
    @app_commands.command(name="setbdaychannel", description="Set the channel where Mai'q will remind you about birthdays!")
    @app_commands.describe(channel="Which channel?")
    async def setbdaychannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        server = interaction.guild

        if not server:
            return await interaction.response.send_message("Mai'q will not listen to you in dms. (Maybe in the future)")

        # self.bot.db_manager.set_birthday_channel(server.id, channel.id)

        await interaction.response.send_message(f"Mai'q will now remind you about birthdays in {channel.mention}.")

    @tasks.loop(seconds=60)
    async def bday_reminder(self):
        today = datetime.now(pytz.timezone('Eire'))
        channel = self.bot.get_channel(1031977836849922111)  # insert your channel id instead
        # in the future, loop through servers and get birthdays for each server

        birthdays = self.bot.db_manager.get_birthdays_for_date(today.day, today.month)
        print(birthdays)

        if not birthdays:
            return
        
        embed = discord.Embed(
            title=f"Birthday{'' if len(birthdays) == 1 else 's'} today!", 
            color=discord.Color.blurple())
        for birthday in birthdays:
            embed.add_field(
                name=pretty_day_month(birthday['day'], birthday['month']), 
                value=f"{birthday['name']}\'s birthday!",
                )
        embed.set_footer(
            text=f"Mai'q will remind you about birthdays every day.")
        
        await channel.send(embed=embed)



async def setup(bot):
    await bot.add_cog(birthdays(bot))