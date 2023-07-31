import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore
from datetime import datetime
import calendar
from pymongo import ASCENDING, DESCENDING

class birthdays_manager:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.collection = self.bot.db['serious_birthdays']
        self.config = self.bot.db['serious_birthdays_config']

    def add_birthday(self, person: str, day: int, month: int, server: discord.Guild, dm_user: discord.User):
        server_id = server.id if server else None
        server_name = server.name if server else None

        self.collection.insert_one({
            "person": person,
            "day": day,
            "month": month,
            "server_id": server_id,
            "server_name": server_name,
            "dm_id": dm_user.id,
            "dm_name": dm_user.name
        })
    
    def get_birthdays(self, server: discord.Guild, dm_user: discord.User):
        if server:
            birthdays =  self.collection.find({
            "server_id": server.id
            })
        else:
            birthdays =  self.collection.find({
            "dm_id": dm_user.id
            })

        birthdays.sort([("month", ASCENDING), ("day", ASCENDING)])

        return birthdays
    
    def create_config_server(self, server: discord.Guild, channel: discord.TextChannel):
        self.config.insert_one({
            "server_id": server.id,
            "server_name": server.name,
            "channel_id": channel.id,
            "channel_name": channel.name,
            "time": 8,
            "timezone": "uhh UTC or something idk how to keep track of that yet",
            "birthdays": []
        })

    def create_config_dm(self, dm_user: discord.User):
        self.config.insert_one({
            "dm_id": dm_user.id,
            "dm_name": dm_user.name,
            "time": 8,
            "timezone": "uhh UTC or something idk how to keep track of that yet",
            "birthdays": []
        })


class birthdays(commands.GroupCog, name="birthday"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.manager = birthdays_manager(bot)
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    @app_commands.command(name="add", description="add a birthday")
    @app_commands.describe(person="Whose birthday?", day="Which day?", month="Which month?")
    async def _add(self, interaction: discord.Interaction, person: str, day: int, month: int):
        try:
            datetime(year=2023, month=month, day=day)
        except ValueError:
            await interaction.response.send_message(f"{day}/{month} is not a valid date.")
            return

        server: discord.Guild = interaction.guild
        dm_user: discord.DMChannel = interaction.user

        self.manager.add_birthday(person, day, month, server, dm_user)
        
        await interaction.response.send_message(f"Added {person}'s birthday on {day}/{month}.")

    @app_commands.command(name="upcoming", description="get upcoming birthdays")
    async def _upcoming(self, interaction: discord.Interaction):
        birthdays = self.manager.get_birthdays(interaction.guild, interaction.user)

        embed = discord.Embed(
            title="Upcoming birthdays:", 
            description="\n".join([f"{birthday['day']}/{birthday['month']} - {birthday['person']}" for birthday in birthdays]),
            color=discord.Color.blurple())
        
        await interaction.response.send_message(embed=embed)
        



async def setup(bot):
    await bot.add_cog(birthdays(bot))