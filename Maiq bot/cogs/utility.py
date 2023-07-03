import discord
from discord.ext import commands
from discord import app_commands
from colorama import Back, Fore, Style
from files import *
import requests
import ast
import os
from dotenv import load_dotenv
load_dotenv()

from cog_base import CogBase


class utility(CogBase, commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
        @commands.Cog.listener()
        async def on_ready(self):
            print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")
    """

    @app_commands.command(name="calculate", description="Mai'q knows math too!")
    @app_commands.describe(expression="Type HELP for a help message")
    async def calculate(self, interaction: discord.Interaction, expression: str):
        if expression.lower() == "help":
            embed = discord.Embed(
                title="Calculator help:",
                description="Write a mathematical expression after /help",
                color=discord.Color.blurple())
            embed.add_field(
                name="Operations:",
                value="""`+` addition
`-` subtraction
`*` multiplication
`/` division
`**` exponentiation""",
                inline=True)
            embed.add_field(
                name="Examples:",
                value="""2+2
3\*\*2 - 9
26 \* (6 - 19)""",
                inline=True)
            return await interaction.response.send_message(embed=embed)
        
        def is_valid(expression: str):
            allowed_chars = set("0123456789.+-*/() ")
            return all(char in allowed_chars for char in expression)

        if not is_valid(expression):
            return await interaction.response.send_message(f"Mai'q won't try to calculate that.")
            
        try:
            await interaction.response.send_message(f"{expression} = {eval(expression)}")
        except Exception as e:
            await interaction.response.send_message(f"Your math is too wacky for Mai'q.")


    @app_commands.command(name="translate", description="Mai's knows many languages")
    @app_commands.describe(translate_from="Translate from", translate_to="Translate to", message="The message you wish to translate")
    async def translate(self, interaction: discord.Interaction, translate_from: str, translate_to: str, message: str):
        first = translate_from.lower()
        second = translate_to.lower()

        if first not in lang_codes and second not in lang_codes:
            await interaction.response.send_message(f"Mai'q knows many languages, but not those.")
            return
        if first not in lang_codes:
            await interaction.response.send_message(f"Mai'q knows many languages, but not **{first}**.")
            return
        if second not in lang_codes:
            await interaction.response.send_message(f"Mai'q knows many languages, but not **{second}**")
            return

        url = "https://translated-mymemory---translation-memory.p.rapidapi.com/get"
        querystring = {
            "langpair": lang_codes[first] + "|" + lang_codes[second],
            "q": message,
            "mt": "1",
            "onlyprivate": "0",
            "de": "a@b.c"}
        headers = {
            "X-RapidAPI-Key": f"{os.getenv('translation_key')}",
            "X-RapidAPI-Host": "translated-mymemory---translation-memory.p.rapidapi.com"}
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        translated_msg = response['responseData']['translatedText']
        # print(response)  # for debugging

        if response['quotaFinished'] is None:
            await interaction.response.send_message("Mai'q might have forgotten one of those languages. Maybe both.")
            return

        embed = discord.Embed(
            color=discord.Color.blurple())
        embed.set_author(
            name="Translation",
            icon_url="https://cdn.discordapp.com/attachments/1060711805028155453/1061411947398045847/Google_Translate_Iconggs.png")
        embed.add_field(
            name=f"From {first}:",
            value=message,
            inline=True)
        embed.add_field(
            name=f"To {second}:",
            value=translated_msg,
            inline=True)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(utility(bot))
