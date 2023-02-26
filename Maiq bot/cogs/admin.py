import discord
from discord.ext import commands
from discord import app_commands
from colorama import Back, Fore, Style
from datetime import datetime
import os
import sys

from discord import ui

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






async def setup(bot):
    await bot.add_cog(admin(bot))
