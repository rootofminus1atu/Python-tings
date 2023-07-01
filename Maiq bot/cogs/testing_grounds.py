import discord
from discord.ext import commands
from discord.ui import Select, View
from discord import app_commands
from colorama import Fore
import gspread
import inflect
p = inflect.engine()



class testing_grounds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    @app_commands.command(name="character", description="Pick the OC you want to see the reference of!")
    async def character(self, interaction: discord.Interaction):
        async def find_row_containing(entry):
            for row in oc_info:
                if row['name'] == entry:
                    return row
            return None
        
        # isolate these 3 lines below somehow somewhere
        sa = gspread.service_account(filename="catwithhorns-fe460388a5f0.json")
        sh = sa.open("Testing")
        wks = sh.worksheet("oc_info")

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
    await bot.add_cog(testing_grounds(bot))
