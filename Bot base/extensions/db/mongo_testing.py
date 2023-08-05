import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore
from typing import Optional
from datetime import datetime

class BaseManager:
    def __init__(self, bot: commands.Bot, collection: str):
        self.bot = bot
        self.collection = self.bot.db[collection]

    async def get_all(self):
        return await self.collection.find({}).to_list(length=None)

    async def delete_all(self):
        await self.collection.delete_many({})

    async def count_all(self):
        return await self.collection.count_documents({})


class BirthdaysManager(BaseManager):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot, collection='birthdays')
    
    async def change_date_for(self, user_id: int, date: datetime):
        await self.collection.update_one({'user_id': user_id}, {'$set': {'date': date}}, upsert=True)

    async def find_by_date(self, date: datetime):
        return await self.collection.find({'date': date}).to_list(length=None)

class UserManager(BaseManager):
    def __init__(self, bot):
        super().__init__(bot, collection='users')

    async def get_all(self):
        return await self.collection.find({}).to_list(length=None)
    
    async def get_aged(self, age: int):
        return await self.collection.find({'age': age}).to_list(length=None)
    
class MainManager:
    def __init__(self, bot):
        self.bot = bot
        self.user = UserManager(bot)
        self.birthday = BirthdaysManager(bot)

async def setup(bot):
    bot.manager = MainManager(bot)