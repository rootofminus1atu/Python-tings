import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from colorama import Fore, Style
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()
import inflect
p = inflect.engine()


from warn_scheme import Warning, WarningsManager, warn_levels

class admin2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings_manager = WarningsManager()

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")


    @app_commands.command(name="warn", description="Warn someone")
    @app_commands.describe(user="Who are you warning", level="How severe the warning is", reason="Why are you warning them")
    @app_commands.choices(level=[
        app_commands.Choice(name=f"{val.emoji} {val.name} = {key} points", value=f"{key}")
        for key, val in warn_levels.items()
    ])
    async def warn(self, interaction: discord.Interaction, user: discord.User, level: app_commands.Choice[str], reason: str):
        # await interaction.response.send_message(f"Warning `{user}` for `{reason}` with `{level} ({type(level)})` points.")
        warning = Warning(
            user.id,
            user.name,
            level.value,
            reason,
            interaction.user.id,
            interaction.user.name,
            interaction.guild.id,
            interaction.guild.name,
            datetime.now()
        )
        print(warning.to_dict())

        warn_level = warn_levels[warning.level]

        embed = discord.Embed(
            color=discord.Color(warn_level.color))
        embed.add_field(
            name=f"{user} has received a {warn_level.emoji} {warn_level.name} {warn_level.emoji} warning.",
            value=f"Reason: {reason}",
            inline=False)
        embed.add_field(
            value=f"{warning.to_dict()}"
        )

        await interaction.response.send_message(embed=embed)

        try:
            await user.send(embed=embed)
        except (discord.Forbidden, discord.HTTPException, AttributeError):
            await interaction.followup.send(f"Could not DM {user.mention}")


    @app_commands.command(name="delwarning", description="Remove a warning")
    @app_commands.describe(id="id of the warning you want to delete")
    async def delwarn2(self, interaction: discord.Interaction, id: str):
        response = self.warnings_manager.try_delete_warning(id, interaction.guild.id)
        await interaction.response.send_message(response)


async def setup(bot):
    await bot.add_cog(admin2(bot))