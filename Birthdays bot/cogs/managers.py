import discord
from discord.ext import commands
from colorama import Fore

class birthdays_manager:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.collection = self.bot.db['serious_birthdays']
        self.config = self.bot.db['serious_birthdays_config']

    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + self.__class__.__name__ + Fore.RESET + " cog loaded")

    def add_birthday(self):
        print("Adding bday!")
        print("ADDING EVEN MORE")

    def get_birthdays(self):
        print("Getting bdays!")

async def setup(bot):
    bot.manager = birthdays_manager(bot)