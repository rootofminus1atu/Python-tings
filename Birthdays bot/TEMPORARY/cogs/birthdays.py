import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore
from datetime import datetime
import calendar
from managers import birthdays_manager


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

        # bruh how do I do this not stupidly
        if self.manager.get_config(server, dm_user) is None:
            config = self.manager.create_config(server, interaction.channel, dm_user)
        
        await interaction.response.send_message(f"Added {person}'s birthday on {day}/{month}.")

    @app_commands.command(name="upcoming", description="get upcoming birthdays")
    async def _upcoming(self, interaction: discord.Interaction):
        birthdays = self.manager.get_birthdays(interaction.guild, interaction.user)
        birthdays_limited = birthdays[:10]

        embed = discord.Embed(
            title="Upcoming birthdays:", 
            description="\n".join([f"{birthday['day']}/{birthday['month']} - {birthday['person']}" for birthday in birthdays_limited]),
            color=discord.Color.blurple())
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="channel", description="set the channel where the bot will send reminders")
    @app_commands.describe(channel="The channel where the bot will send reminders")
    async def _channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        self.manager.set_channel(interaction.guild, channel)
        await interaction.response.send_message(f"Set channel to {channel.mention}")
        



async def setup(bot):
    await bot.add_cog(birthdays(bot))