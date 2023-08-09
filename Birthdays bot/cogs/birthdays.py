import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore
from datetime import datetime
import calendar
import pymongo
import pytz
import zoneinfo
import tzdata


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
# - _time command autocompletion with timezones
# - maybe replace _time and _channel with _mode and add more functionality

# REMINDER TO CHECK THIS
time_stuff = [str(n) for n in range(24)]

timezones = [
    ("GMT", "Countries like: Ireland, Portugal, Morocco"),
    ("PST", "California, Oregon, Washington"),
    ("CST", "Texas, Illinois, Minnesota"),
]

class Embeds:
    @staticmethod
    def added_birthday(birthday: dict):
        embed = discord.Embed(
            title=f"Added {birthday['person']}'s birthday on {birthday['day']}/{birthday['month']}",
            color=discord.Color.random()
        )
        return embed


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
        embed = Embeds.added_birthday(birthday)

        # TODO:
        # change the embed texts and include the proper channel
        
        if not await self.bot.manager.get_config(interaction):
            new_config = await self.bot.manager.create_config(interaction, and_birthday=birthday)

            if interaction.guild:
                embed.description = f"Configuration was created. Currently birthdays will be sent at 8am UTC in {new_config['channel']}. Change them using `/birthday channel` and `/birthday time`."
            else:
                embed.description = f"Configuration was created. Currently birthdays will be sent at 8am UTC. Change it using `/birthday time`."
            
            await interaction.response.send_message(embed=embed)
            return


        if await self.bot.manager.get_config_from_person_birthday(interaction, person):
            await interaction.response.send_message(f"{person}'s birthday already exists.")
            return
        

        await self.bot.manager.add_birthday(interaction, birthday)

        if interaction.guild:
            embed.description = f"Await birthdays to be sent at 8am UTC in {interaction.channel.mention}. Change them using `/birthday channel` and `/birthday time`."
        else:
            embed.description = f"Await birthdays to be sent at 8am UTC. Change it using `/birthday time`."

        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="upcoming", description="get upcoming birthdays")
    async def _upcoming(self, interaction: discord.Interaction):
        birthdays = await self.bot.manager.get_birthdays(interaction)

        if not birthdays:
            await interaction.response.send_message("There are no birthdays.")
            return

        # format them better, order in a chronological order based on the datetime

        formatted_birthdays = [
            f"{birthday['person']} - {birthday['day']}/{birthday['month']}"
            for birthday in birthdays[:10]
        ]

        embed = discord.Embed(
            title="Upcoming birthdays",
            description="\n".join(formatted_birthdays),
            color=discord.Color.random()
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="remove", description="remove a birthday")
    @app_commands.describe(person="Whose birthday?")
    async def _remove(self, interaction: discord.Interaction, person: str):
        if not await self.bot.manager.get_config(interaction):
            await interaction.response.send_message("There are no birthdays.")
            return

        if not await self.bot.manager.get_birthday_from_person(interaction, person):
            await interaction.response.send_message(f"{person}'s birthday doesn't exist.")
            return

        await self.bot.manager.remove_birthday(interaction, person)
        await interaction.response.send_message(f"Removed {person}'s birthday.")

    @app_commands.command(name="channel", description="change the channel where birthdays are announced")
    @app_commands.describe(channel="The channel where birthdays are announced")
    async def _channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        situation = self.bot.helpers.get_situation(interaction)
        
        if not interaction.guild:
            await interaction.response.send_message("This command can only be used in servers.")
            return
        
        await self.bot.manager.update_config_channel(situation, channel)
        await interaction.response.send_message(f"Set birthdays channel to {channel.mention}")
        



    @app_commands.command(name="time", description="change the time when birthdays are announced")
    @app_commands.describe(time="The time when birthdays are announced", timezone="The timezone")
    @app_commands.choices(time=[
        app_commands.Choice(name=f"{item}:00", value=f"{item}")
        for item in time_stuff
    ])
    @app_commands.choices(timezone=[
        app_commands.Choice(name=f"{item[0]} ({item[1]})", value=f"{item[0]}")
        for item in timezones
    ])
    async def _time(self, interaction: discord.Interaction, time: app_commands.Choice[str], timezone: app_commands.Choice[str]):
        situation = self.bot.helpers.get_situation(interaction)

        chosen_time = int(time.value)
        chosen_timezone = timezone.value

        if not await self.bot.manager.get_config(situation):
            await self.bot.manager.create_config(situation, time=chosen_time, timezone=chosen_timezone)
            await interaction.response.send_message(f"Set birthdays time to {chosen_time} {chosen_timezone}")
            return

        await self.bot.manager.update_config_time(situation, chosen_time, chosen_timezone)
        await interaction.response.send_message(f"Set birthdays time to {chosen_time} {chosen_timezone}")


async def setup(bot):
    await bot.add_cog(birthdays(bot))