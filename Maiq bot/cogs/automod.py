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




class automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.automod_tracker = self.bot.db_manager.automod_manager

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
        occurrence = self.automod_tracker.manage_increment_and_get_count(message.guild.id, message.author.id)

        channel = self.bot.get_channel(automod_channel_id)
        await channel.send(embed=automod_embed(word, message, severity, occurrence))

        if severity == "PROHIBITED":
            await message.delete()
        

                

async def setup(bot):
    await bot.add_cog(automod(bot))