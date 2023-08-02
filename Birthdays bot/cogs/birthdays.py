import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore
from datetime import datetime
import calendar
import pymongo


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

        # either server
        server = interaction.guild
        channel = interaction.channel
        # or dm
        user = interaction.user

        if server:
            situation = server
        else:
            situation = user

        # check if server or dm
        if server:
            if not self.collection.find_one({"server_id": server.id}):
                self.collection.insert_one({
                    "server_id": server.id,
                    "server_name": server.name,
                    "channel_id": channel.id,
                    "channel_name": channel.name,
                    "time": "8:00",
                    "timezone": "UTC",
                    "birthdays": [birthday]
                })
                await interaction.response.send_message(f"Added {person}'s birthday on {day}/{month}.")
                return
            
            # check if bday already exists
            if self.collection.find_one({"server_id": server.id, "birthdays": {"$elemMatch": {"person": person}}}):
                await interaction.response.send_message(f"{person}'s birthday already exists.")
                return
            
            # add bday
            self.collection.update_one({"server_id": server.id}, {"$push": {
                "birthdays": {
                    "person": person,
                    "day": day,
                    "month": month
                }
            }})
            await interaction.response.send_message(f"Added {person}'s birthday on {day}/{month}.")
            return
        else:
            config = self.collection.find_one({"user_id": user.id})
            if not config:
                self.collection.insert_one({
                    "user_id": user.id,
                    "user_name": user.name,
                    "time": "8:00",
                    "timezone": "UTC",
                    "birthdays": [birthday]
                })
                await interaction.response.send_message(f"Added {person}'s birthday on {day}/{month}.")
                return
            
            # check if bday already exists
            if self.collection.find_one({"user_id": user.id, "birthdays": {"$elemMatch": {"person": person}}}):
                await interaction.response.send_message(f"{person}'s birthday already exists.")
                return
            
            # add bday
            self.collection.update_one({"user_id": user.id}, {"$push": {
                "birthdays": {
                    "person": person,
                    "day": day,
                    "month": month
                }
            }})
            await interaction.response.send_message(f"Added {person}'s birthday on {day}/{month}.")
            return

    @app_commands.command(name="upcoming", description="get upcoming birthdays")
    async def _upcoming(self, interaction: discord.Interaction):
        await interaction.response.send_message("showing 10 bdays")

    @app_commands.command(name="channel", description="change the channel where birthdays are announced")
    @app_commands.describe(channel="The channel where birthdays are announced")
    async def _channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        await interaction.response.send_message(f"Set birthdays channel to {channel.mention}")

    @app_commands.command(name="time", description="change the time when birthdays are announced")
    @app_commands.describe(time="The time when birthdays are announced", timezone="The timezone of the time")
    async def _time(self, interaction: discord.Interaction, time: str, timezone: str):
        # change timezone to a choice menu
        await interaction.response.send_message(f"Set birthdays time to {time} {timezone}")


async def setup(bot):
    await bot.add_cog(birthdays(bot))