import discord
from discord.ext import commands
from discord.ui import Select, View
from discord import app_commands
from colorama import Fore
import gspread
import inflect
p = inflect.engine()

sa = gspread.service_account(filename="catwithhorns-fe460388a5f0.json")
sh = sa.open("Testing")

wks = sh.worksheet("oc_info")

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    @app_commands.command(name="serverinfo", description="Inforomation about the server!")
    async def serverinfo(self, interaction: discord.Interaction):
        role_list = [str(role.name) for role in interaction.guild.roles if role.name != "@everyone"]
        co_owner_role = interaction.guild.get_role(1061762185971368019)
        creation_time = interaction.guild.created_at

        try:
            co_owners = ", ".join(str(member) for member in co_owner_role.members if member != interaction.guild.owner)
        except:
            co_owners = "Nobody!"

        embed = discord.Embed(
            title="Server information",
            description=f"""🔹**Name:** {interaction.guild.name}
🔹**Id:** {interaction.guild.id}
🔹**Owner:** {interaction.guild.owner}
🔹**Co-owner(s):** {co_owners}""",
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
        try:
            icon_url = interaction.guild.icon.url
            embed.set_thumbnail(url=icon_url)
        except:
            pass
        embed.set_footer(
            # ugliest datetime formatting code ever
            text=f"""Server creation date: {creation_time.strftime(f'{p.ordinal(creation_time.strftime("%d"))} %B %Y')}""")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="botinfo", description="Info about the bot")
    async def botinfo(self, interaction: discord.Interaction):
        creation_time = self.bot.user.created_at
        bot_info = await self.bot.application_info()
        owner = bot_info.owner

        embed = discord.Embed(
            title=f"{self.bot.user}",
            description=f"M'aiq knows much, tells some. M'aiq knows many things others do not.",
            color=discord.Color.blurple())
        embed.set_thumbnail(
            url=f"{self.bot.user.avatar.url}")
        embed.add_field(
            name="Dev:",
            value=f"{owner.name}#{owner.discriminator}",
            inline=True)
        embed.add_field(
            name="Library:",
            value=f"discord.py version {discord.__version__}",
            inline=True)
        embed.set_footer(
            text=f"""Creation date: {creation_time.strftime(f'{p.ordinal(creation_time.strftime("%d"))} %B %Y')}""")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="character", description="Pick the OC you want to see the reference of!")
    async def character(self, interaction: discord.Interaction):
        async def find_row_containing(entry):
            for row in oc_info:
                if row['name'] == entry:
                    return row
            return None

        oc_info = wks.get_all_records()

        select = Select(
            placeholder="Choose an oc to display!",
            options=[discord.SelectOption(
                label=oc['name'],
                emoji=oc["emoji"],
                description=oc["short_description"])
                for oc in oc_info]
        )

        embed = discord.Embed(
            title="Select an OC from below to see their info!",
            color=discord.Color.blurple(), )
        embed.set_author(
            name="Character info",
            icon_url=discord.PartialEmoji.from_str(oc_info[0]["emoji"]).url)

        view = View(timeout=60)
        view.add_item(select)

        async def my_callback(interaction):
            oc = await find_row_containing(select.values[0])

            embed = discord.Embed(
                title=oc['name'],
                description=oc['description'],
                color=discord.Color.from_str(oc["side_color"]))
            embed.set_author(
                name="Character info",
                icon_url=discord.PartialEmoji.from_str(oc["emoji"]).url)
            embed.add_field(
                name="Created by:",
                value=oc["created_by"],
                inline=True)
            embed.add_field(
                name="Created on:",
                value=oc["created_on"],
                inline=True)
            embed.set_image(url=oc["image"])
            embed.set_footer(text="You can select another OC from the dropdown menu below!")

            await interaction.response.edit_message(view=view, embed=embed)

        select.callback = my_callback

        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(info(bot))
