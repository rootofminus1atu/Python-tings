import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore
from datetime import datetime
from enum import Enum

from files import prohibited_words, dangerous_words, automod_channel_id, HOME_ID
from helpers import pretty_date, ordinal


def automod_embed(word: str, message: discord.Message, severity, occurrence: int):
    severity_map = {
        "DANGEROUS": discord.Color.orange(),
        "PROHIBITED": discord.Color.red()
    }

    embed = discord.Embed(
        title=f"{severity.title()} word __{word}__ detected in message{f' ({message.jump_url})' if severity == 'DANGEROUS' else ''}",
        description=f"{message.content}",
        color=severity_map[severity])
    embed.set_author(
        name=f"{ordinal(occurrence)} occurance for {message.author.name}",
        icon_url=message.author.avatar.url)
    embed.set_footer(
        text=pretty_date(datetime.now()))
    
    return embed


class automod(commands.GroupCog, name="automod"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()
        self.automod_manager = self.bot.db_manager.automod_manager

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        # automoding only in 1 server for now
        if message.guild is not None and message.guild.id == HOME_ID:
            for word in dangerous_words:
                if word in message.content:
                    await self.handle_automod_situation(message, word, "DANGEROUS")
                    return

            for word in prohibited_words:
                if word in message.content:
                    await self.handle_automod_situation(message, word, "PROHIBITED")
                    return
            
    async def handle_automod_situation(self, message: discord.Message, word: str, severity):
        occurrence = self.automod_manager.increment_record_and_get_count(message.guild.id, message.author.id)

        channel = self.bot.get_channel(automod_channel_id)
        await channel.send(embed=automod_embed(word, message, severity, occurrence))

        if severity == "PROHIBITED":
            await message.delete()

    @app_commands.command(name="channel", description="Pick a channel for automod to send messages to")
    @app_commands.describe(channel="The channel to send automod messages to")
    async def _channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        self.automod_manager.update_config_channel(interaction.guild.id, interaction.guild.name, channel.id, channel.name)
        await interaction.response.send_message(f"Automod channel set to {channel.mention}")


    @app_commands.command(name="add_dangerous_word", description="Add a dangerous word to the automod list")
    @app_commands.describe(word="The word to add")
    async def _add_dangerous_word(self, interaction: discord.Interaction, word: str):
        self.automod_manager.add_dangerous_word(interaction.guild.id, word)
        await interaction.response.send_message(f"Added {word} to the dangerous words list")

    
    @app_commands.command(name="add_prohibited_word", description="Add a prohibited word to the automod list")
    @app_commands.describe(word="The word to add")
    async def _add_prohibited_word(self, interaction: discord.Interaction, word: str):
        self.automod_manager.add_prohibited_word(interaction.guild.id, word)
        await interaction.response.send_message(f"Added {word} to the prohibited words list")

    
    @app_commands.command(name="see_words", description="See the list of dangerous and prohibited words")
    async def _see_words(self, interaction: discord.Interaction):
        config = self.automod_manager.get_config(interaction.guild.id)
        dangerous_words = config['dangerous_words']
        prohibited_words = config['prohibited_words']

        await interaction.response.send_message(f"**Dangerous words:** {', '.join(dangerous_words)}\n**Prohibited words:** {', '.join(prohibited_words)}")



    @app_commands.command(name="ping", description="...")
    async def _ping(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("pong!")

    @app_commands.command(name="command", description="...")
    async def _cmd(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("automodding time")


        

                

async def setup(bot):
    await bot.add_cog(automod(bot))