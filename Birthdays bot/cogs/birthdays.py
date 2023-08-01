import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore
from datetime import datetime
import calendar


class birthdays(commands.GroupCog, name="birthday"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    @app_commands.command(name="add", description="add a birthday")
    @app_commands.describe(person="Whose birthday?", day="Which day?", month="Which month?")
    async def _add(self, interaction: discord.Interaction, person: str, day: int, month: int):
        await interaction.response.send_message(f"Added {person}'s birthday on {day}/{month}.")

    @app_commands.command(name="upcoming", description="get upcoming birthdays")
    async def _upcoming(self, interaction: discord.Interaction):
        await interaction.response.send_message("showing 10 bdays")


async def setup(bot):
    await bot.add_cog(birthdays(bot))