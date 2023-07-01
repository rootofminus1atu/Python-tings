import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore, Style
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

from warn_scheme import Warning, WarningsManager, warn_levels
from errors import *
from files import *
from helpers import pretty_date


class admin2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings_manager = WarningsManager()

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")


    @has_mod_or_roles(special_roles)
    @app_commands.command(name="say", description="What will Mai'q speak? Where shall he speak?")
    @app_commands.describe(text="What I'll say:", channel="Where I'll say it:")
    async def say(self, interaction: discord.Interaction, text: str, channel: discord.TextChannel):
        await channel.send(text)
        await interaction.response.send_message("Mai'q spoke.", ephemeral=True)


    @commands.command(aliases=['close', 'kill'])
    async def shutdown(self, ctx):
        if ctx.author.guild_permissions.administrator:
            now = datetime.now()
            prfx = Fore.BLACK + Style.BRIGHT + now.strftime('%Y-%m-%d %H:%M:%S')
            prfx += Fore.LIGHTBLUE_EX + " INFO\t" + Fore.RESET + Style.RESET_ALL
            print(prfx + Fore.MAGENTA + f" {ctx.author}" + Fore.RED + " shutdown the bot" + Fore.RESET)
            await ctx.send("It's getting late. Mai'q is going to bed.")
            await self.bot.close()
        else:
            await ctx.send("Mai'q will not listen to you.")


    @has_mod_or_roles(special_roles)
    @app_commands.command(name="warn", description="Warn someone")
    @app_commands.describe(user="Who are you warning", level="How severe the warning is", reason="Why are you warning them")
    @app_commands.choices(level=[
        app_commands.Choice(name=f"{val.emoji} {val.name} = {key} points", value=f"{key}")
        for key, val in warn_levels.items()
    ])
    async def warn(self, interaction: discord.Interaction, user: discord.User, level: app_commands.Choice[str], reason: str):
        warn_level = warn_levels[int(level.value)]

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
        # print(warning.to_dict())
        self.warnings_manager.add_warning(warning)

        embed = discord.Embed(
            color=discord.Color(warn_level.color))
        embed.add_field(
            name=f"{user} has received a {warn_level.emoji} {warn_level.name} {warn_level.emoji} warning.",
            value=f"Reason: {reason}",
            inline=False)
        """embed.add_field(
            name="Warning dict",
            value=f"{warning.to_dict()}"
        )"""

        await interaction.response.send_message(embed=embed)

        try:
            await user.send(embed=embed)
        except (discord.Forbidden, discord.HTTPException, AttributeError):
            await interaction.followup.send(f"Could not DM {user.mention}")


    @has_mod_or_roles(special_roles)
    @app_commands.command(name="warnings", description="Check how many warnings a user has")
    @app_commands.describe(user="Whose warnings do you want to see")
    async def warnings(self, interaction: discord.Interaction, user: discord.User):
        server = interaction.guild  # add if else check for dm thing
        if server is None:
            return await interaction.response.send_message("This command can only be used in a server.")
        
        expiration_time = timedelta(seconds=self.warnings_manager.get_ttl())

        def get_side_color(severity):
            max_severity = list(warn_levels.keys())[-1]
            
            while severity not in warn_levels:
                if severity > max_severity:
                    return max_severity
                severity += 1
            
            return severity
        
        all_warnings = self.warnings_manager.get_warnings(user.id, server.id)
        how_many = len(all_warnings)
        severity = sum([warning.level for warning in all_warnings]) 
        side_color = get_side_color(severity)

        embed = discord.Embed(
            color=discord.Color(warn_levels[side_color].color))
        embed.set_author(
            name=f"{how_many} warning{'' if how_many == 1 else 's'} for {user.display_name}",
            icon_url=user.avatar.url)
        embed.add_field(
            name="Severity:",
            value=f"{severity}/7",
            inline=False)
        for warning in all_warnings:
            warning_date = warning.created_at  # fix this
            date_str = pretty_date(warning_date)

            exp_date = warning_date + expiration_time
            exp_str = pretty_date(exp_date)

            fat_discord_mod = await self.bot.fetch_user(warning.mod_id)

            embed.add_field(
                name=f"{warn_levels[warning.level].emoji} +{warning.level} | ID: {warning._id} | Moderator: {fat_discord_mod}",
                value=f"Reason: {warning.reason}\nDate: {date_str}\nExpires: {exp_str}",
                inline=False)

        await interaction.response.send_message(embed=embed)


    @has_mod_or_roles(special_roles)
    @app_commands.command(name="delwarning", description="Remove a warning")
    @app_commands.describe(id="id of the warning you want to delete")
    async def delwarn(self, interaction: discord.Interaction, id: str):
        server = interaction.guild

        if server is None:
            return await interaction.response.send_message("This command can only be used in a server.")
        
        found_warning = self.warnings_manager.try_get_warning(id, server.id)

        if found_warning is None:
            return await interaction.response.send_message(f"Warning with id `{id}` not found.")

        self.warnings_manager.delete_warning(found_warning)
        await interaction.response.send_message("Deleted warning with id `{id}` for user {found_warning.user_name}")


async def setup(bot):
    await bot.add_cog(admin2(bot))