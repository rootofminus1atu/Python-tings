import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore
from datetime import datetime
import calendar
import pymongo

# NOTE:
# `if not birthdays`
# `if birthdays is None`
# those are actually different
# the first one activates not only in None cases, but also in empty lists, empty dicts, empty strings, etc
# the second one only activates in None cases
# which actually makes sense, I should keep that in mind

# TODO:
# - improve the _add command (into an embed, more info, add channel info)
# - add birthday _update command
# - make the _time command work

class birthdays(commands.GroupCog, name="birthday"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.collection = self.bot.db['serious_birthdays_config']
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    @app_commands.command(name="add", description="add a birthday")
    @app_commands.describe(person="Whose birthday?", day="Which day?", month="Which month?")
    async def _add(self, interaction: discord.Interaction, person: str, day: int, month: int):
        # datetime validation
        try:
            datetime(year=2000, month=month, day=day)
            # oh yeah 29th feb people need a special case omfg
        except ValueError:
            await interaction.response.send_message("Invalid date.")
            return
        
        birthday = {
            "person": person,
            "day": day,
            "month": month
        }

        situation = self.bot.helpers.get_situation(interaction)

        # reminder:
        # add cases for servers and dms, channel vs no channel
        if not self.bot.manager.get_config(situation):
            new_config = self.bot.manager.create_config(situation, and_birthday=birthday)
            await interaction.response.send_message(f"Added {person}'s birthday on {day}/{month}. Configuration was created. Currently birthdays will be sent at 8am UTC. Change them using `/birthday channel` and `/birthday time`. (I might add a `/birthday mode` instead in the future)")
            return
        
        if self.bot.manager.get_config_from_person_birthday(situation, person):
            await interaction.response.send_message(f"{person}'s birthday already exists.")
            return
        
        self.bot.manager.add_birthday(situation, birthday)
        await interaction.response.send_message(f"Added {person}'s birthday on {day}/{month}. Await birthdays to be sent at 8am UTC. Change them using `/birthday channel` and `/birthday time`. (I might add a `/birthday mode` instead in the future)")


    @app_commands.command(name="upcoming", description="get upcoming birthdays")
    async def _upcoming(self, interaction: discord.Interaction):
        situation = self.bot.helpers.get_situation(interaction)

        birthdays = self.bot.manager.get_birthdays(situation)
         
        if not birthdays:
            await interaction.response.send_message("There are no birthdays.")
            return
    
        embed = discord.Embed(
            title="Upcoming birthdays", 
            description="\n".join([f"{birthday['person']} - {birthday['day']}/{birthday['month']}" for birthday in birthdays[:10]]),
            color=discord.Color.random())

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="remove", description="remove a birthday")
    @app_commands.describe(person="Whose birthday?")
    async def _remove(self, interaction: discord.Interaction, person: str):
        situation = self.bot.helpers.get_situation(interaction)

        if not self.bot.manager.get_config(situation):
            await interaction.response.send_message("There are no birthdays.")
            return

        if not self.bot.manager.get_birthday_from_person(situation, person):
            await interaction.response.send_message(f"{person}'s birthday doesn't exist.")
            return

        self.bot.manager.remove_birthday(situation, person)
        await interaction.response.send_message(f"Removed {person}'s birthday.")

    @app_commands.command(name="channel", description="change the channel where birthdays are announced")
    @app_commands.describe(channel="The channel where birthdays are announced")
    async def _channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        situation = self.bot.helpers.get_situation(interaction)
        
        if not interaction.guild:
            await interaction.response.send_message("This command can only be used in servers.")
            return
        
        self.bot.manager.update_config_channel(situation, channel)
        await interaction.response.send_message(f"Set birthdays channel to {channel.mention}")
        

    time_stuff = [
        ("8"),
        ("9"),
        ("10")
    ]

    timezones = [
        ("UTC", "UK, Portugal, Morocco, etc."),
        ("UTC+1", "France, Poland, Chroatia, etc.")
    ]

    @app_commands.command(name="time", description="change the time when birthdays are announced")
    @app_commands.describe(time="The time when birthdays are announced", timezone="The timezone")
    @app_commands.choices(time=[
        app_commands.Choice(name=f"{item}:00", value=f"{item}")
        for item in time_stuff
    ])
    @app_commands.choices(timezone=[
        app_commands.Choice(name=f"{item[0]} - {item[1]}", value=f"{item[0]}")
        for item in timezones
    ])
    async def _time(self, interaction: discord.Interaction, time: app_commands.Choice[str], timezone: app_commands.Choice[str]):
        # changing the time and timezone in the db
        await interaction.response.send_message(f"Set birthdays time to {time.value} {timezone.name}")


async def setup(bot):
    await bot.add_cog(birthdays(bot))