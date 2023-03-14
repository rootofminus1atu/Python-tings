import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from colorama import Back, Fore, Style
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()
import inflect
p = inflect.engine()

from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId

from testing import add_warn, get_ttl, get_warns



CONNECTION_STRING = f"mongodb+srv://RootOfMinus1:{os.getenv('MANGO')}@cluster0.ccfbwh6.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)

db = client.get_database('CatWithHorns')
warnings = db.warnings

class WarnLevel:
    def __init__(self, emoji, color, name):
        self.emoji = emoji
        self.color = color
        self.name = name

warn_levels = {
    0: WarnLevel("🔵", 0x55ACEE, "Verbal"),
    1: WarnLevel("🟢", 0x78B159, "Normal"),
    3: WarnLevel("🟡", 0xFDCB58, "Medium"),
    5: WarnLevel("🟠", 0xF4900C, "Big"),
    7: WarnLevel("🔴", 0xDD2E44, "Huge"),
    10: WarnLevel("⚫", 0x000000, "`nil`")
}


class MyModal(ui.Modal, title="ok"):
    name = ui.TextInput(
        label="Name",
        placeholder="name your goober",
        style=discord.TextStyle.short)
    description = ui.TextInput(
        label="hi",
        placeholder="idk what",
        style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{self.name}")


class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    @app_commands.command(name="say", description="What will Mai'q speak? Where shall he speak?")
    @app_commands.describe(text="What I'll say:", channel="Where I'll say it:")
    async def say(self, interaction: discord.Interaction, text: str, channel: discord.TextChannel):
        if interaction.user.guild_permissions.administrator:
            await channel.send(text)
            await interaction.response.send_message("Mai'q spoke.", ephemeral=True)
        else:
            await interaction.response.send_message("Mai'q won't listen to you.", ephemeral=True)

    @commands.command(aliases=['close', 'kill'])
    # @commands.has_permissions(administrator=True)  # how error handling
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

    @app_commands.command(name="modal")
    async def modal(self, interaction: discord.Interaction):
        await interaction.response.send_modal(MyModal())

    @app_commands.command(name="warnings", description="Check how many warnings a user has")
    @app_commands.describe(user="The user")
    async def warnings(self, interaction: discord.Interaction, user: discord.User):
        warns = get_warns(user.id)

        expiration_time = timedelta(seconds=get_ttl(warnings))

        severity = sum([int(warn['warn_level']) for warn in warns])

        side_col = severity
        while side_col not in warn_levels:
            if side_col > 10:
                side_col = 10
                break
            side_col += 1

        embed = discord.Embed(
            color=discord.Color(warn_levels[side_col].color))
        embed.set_author(
            name=f"{len(warns)} warnings for {user}",
            icon_url=user.avatar.url)
        embed.add_field(
            name="Severity:",
            value=f"{severity}/7",
            inline=False)
        for warn in warns:
            warn_date = warn['created_at']
            date_str = f"""{warn_date.strftime(f'{p.ordinal(warn_date.strftime("%d"))} %B %Y')}"""

            exp_date = warn_date + expiration_time
            exp_str = f"""{exp_date.strftime(f'{p.ordinal(exp_date.strftime("%d"))} %B %Y')}"""

            embed.add_field(
                name=f"{warn_levels[warn['warn_level']].emoji} +{warn['warn_level']} | ID: {warn['_id']} | Moderator: {warn['warned_by']}",
                value=f"Reason: {warn['reason']}\nDate: {date_str}\nExpires: {exp_str}",
                inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="warn", description="Warn someone")
    @app_commands.describe(user="The user", level="How severe the warn is", reason="What reason")
    @app_commands.choices(level=[
        app_commands.Choice(name=f"{value.emoji} {value.name} = {key} points", value=f"{key}")
        for key, value in warn_levels.items()
    ])
    async def warn(self, interaction: discord.Interaction, user: discord.User, level: app_commands.Choice[str], reason: str):
        add_warn(user.id, reason, level.value, interaction.user)

        lvl = warn_levels[int(level.value)]

        embed = discord.Embed(
            color=discord.Color(lvl.color))
        embed.add_field(
            name=f"{user} has received a {lvl.emoji} {lvl.name} {lvl.emoji} warning.",
            value=f"Reason: {reason}",
            inline=False)

        await interaction.response.send_message(embed=embed)

        try:
            await user.send(embed=embed)
        except discord.Forbidden:
            await interaction.followup.send(f"Could not DM {user.mention}")


    @app_commands.command(name="delwarn", description="Remove a warning")
    @app_commands.describe(id="id of the warning you want to delete")
    async def delwarn(self, interaction: discord.Interaction, id: str):
        try:
            object_id = ObjectId(id)
        except (InvalidId, TypeError):
            await interaction.response.send_message(f"Invalid warning id: {id}")
            return

        warn = warnings.find_one({"_id": object_id})
        if warn is None:
            await interaction.response.send_message(f"Warning with id {id} not found.")
        else:
            warnings.delete_one({"_id": object_id})
            await interaction.response.send_message(f"Deleted warning with id {id}")









async def setup(bot):
    await bot.add_cog(admin(bot))
