import discord
from discord.ext import commands
from discord.ui import Select, View
from discord import app_commands
from colorama import Fore
import inflect
p = inflect.engine()

from helpers import pretty_date, get_user_from_id
from files import co_owner_role_id
from bot_dev_scheme import BotDev

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    @app_commands.command(name="serverinfo", description="Inforomation about the server!")
    async def serverinfo(self, interaction: discord.Interaction):
        role_list = [str(role.name) for role in interaction.guild.roles if role.name != "@everyone"]
        
        co_owner_role = interaction.guild.get_role(co_owner_role_id)
        if co_owner_role is not None:
            co_owners = [str(member) for member in co_owner_role.members if member != interaction.guild.owner]
        else:
            co_owners = []

        embed = discord.Embed(
            title="Server information",
            description=f"""🔹**Name:** {interaction.guild.name}
🔹**Id:** {interaction.guild.id}
🔹**Owner:** {interaction.guild.owner}
🔹**{"Co-owner" if len(co_owners) == 1 else "Co-owners"}:** {", ".join(co_owners) if len(co_owners) != 0 else "Nobody!"}""",
            color=discord.Color.blurple())
        embed.add_field(
            name="Members:",
            value=f"""🔹**All:** {len(interaction.guild.members)}
🔹**Online:** {sum(member.status != discord.Status.offline for member in interaction.guild.members)}""",
            inline=True)
        embed.add_field(
            name="Channels:",
            value=f"""🔹**Text:** {len(interaction.guild.text_channels)}
🔹**Voice:** {len(interaction.guild.voice_channels)}""",
            inline=True)
        embed.add_field(
            name=f"Roles ({len(role_list)}):",
            value=", ".join(role_list),
            inline=False)
        embed.set_footer(
            # ugliest datetime formatting code ever
            text=f"Server creation date: {pretty_date(interaction.guild.created_at)}")
        if interaction.guild.icon is not None:
            icon_url = interaction.guild.icon.url
            embed.set_thumbnail(url=icon_url)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="botinfo", description="Info about the bot")
    async def botinfo(self, interaction: discord.Interaction):
        bot_info = await self.bot.application_info()

        embed = discord.Embed(
            title=f"{self.bot.user.name}",
            description=f"M'aiq knows much, tells some. M'aiq knows many things others do not.",
            color=discord.Color.blurple())
        embed.set_thumbnail(
            url=f"{self.bot.user.avatar.url}")
        embed.add_field(
            name="Dev:",
            value=f"{bot_info.owner}",
            inline=True)
        embed.add_field(
            name="Library:",
            value=f"discord.py version {discord.__version__}",
            inline=True)
        embed.set_footer(
            text=f"Creation date: {pretty_date(self.bot.user.created_at)}")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ourdevs", description="Get a list of the bot devs")
    async def ourdevs(self, interaction: discord.Interaction):
        # better fetch stuff here or in the BotDev class? idk
        bot_info = await self.bot.application_info()
        notables = BotDev.get_users()
        print(notables)
        devs = [await get_user_from_id(self.bot, user.id) for user in notables if user.dev]
        devs_filtered = [dev.name for dev in devs if dev is not None]
        testers = [await get_user_from_id(self.bot, user.id) for user in notables if user.tester]
        testers_filtered = [tester.name for tester in testers if tester is not None]
        print(devs)
        print(testers)

        embed = discord.Embed(
            title="Our devs",
            description="Here are the devs of this bot!",
            color=discord.Color.blurple())
        embed.add_field(
            name="Owner:",
            value=f"**{bot_info.owner}**",
            inline=True)
        embed.add_field(
            name="Devs:",
            value=", ".join(devs_filtered),
            inline=True)
        embed.add_field(
            name="Testers:",
            value=", ".join(testers_filtered),
            inline=True)
        
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(info(bot))
