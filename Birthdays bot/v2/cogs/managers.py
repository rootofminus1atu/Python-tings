import discord
from discord.ext import commands
from colorama import Fore
from typing import Optional

DEFAULT_TIME = 8
DEFAULT_TIMEZONE = "UTC"
# UTC contains countries like England, Portugal, Ghana, Morocco, Iceland, etc.


class birthdays_manager:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.collection = self.bot.db['serious_birthdays_config']

    def create_config_server(self, server: discord.Guild, channel: discord.TextChannel, time=DEFAULT_TIME, timezone=DEFAULT_TIMEZONE):
        self.collection.insert_one({
            "server_id": server.id,
            "server_name": server.name,
            "channel_id": channel.id,
            "channel_name": channel.name,
            "time": time,
            "timezone": timezone,
            "birthdays": [] 
        })

    def create_config_server_with_birthday(self, server: discord.Guild, channel: discord.TextChannel, birthday: dict):
        self.collection.insert_one({
            "server_id": server.id,
            "server_name": server.name,
            "channel_id": channel.id,
            "channel_name": channel.name,
            "time": "8:00",
            "timezone": "UTC",
            "birthdays": [birthday]
        })

    def get_person_birthday_server(self, server: discord.Guild, person: str) -> Optional[dict]:
        return self.collection.find_one({"server_id": server.id, "birthdays": {"$elemMatch": {"person": person}}})

    def get_config_server(self, server: discord.Guild) -> Optional[dict]:
        return self.collection.find_one({"server_id": server.id})
    
    def update_config_server(self, server: discord.Guild, channel: discord.TextChannel, time=DEFAULT_TIME, timezone=DEFAULT_TIMEZONE):
        if not self.get_config_server(server):
            self.create_config_server(server, channel, time, timezone)
            return

        self.collection.update_one({"server_id": server.id}, {"$set": {
            "channel_id": channel.id,
            "channel_name": channel.name,
            "time": time,
            "timezone": timezone
        }})

    def create_config_dm(self, user: discord.User, time=DEFAULT_TIME, timezone=DEFAULT_TIMEZONE):
        self.collection.insert_one({
            "user_id": user.id,
            "user_name": user.name,
            "time": time,
            "timezone": timezone,
            "birthdays": []
        })

    def get_config_dm(self, user: discord.User) -> Optional[dict]:
        return self.collection.find_one({"user_id": user.id})
    
    def update_config_dm(self, user: discord.User, time=DEFAULT_TIME, timezone=DEFAULT_TIMEZONE):
        if not self.get_config_dm(user):
            self.create_config_dm(user, time, timezone)
            return

        self.collection.update_one({"user_id": user.id}, {"$set": {
            "time": time,
            "timezone": timezone
        }})

    def add_birthday_server(self, server: discord.Guild, day, month, person):
        if not self.get_config_server(server):
            self.create_config_server(server)

            self.insert_one({
                "server_id": server.id,
                "server_name": server.name,

            })

        self.collection.update_one({"server_id": server.id}, {"$push": {
            "birthdays": {
                "day": day,
                "month": month,
                "person": person
            }
        }})

    def add_birthday_dm(self, user: discord.User, day, month, person):
        if not self.get_config_dm(user):
            self.create_config_dm(user)

        self.collection.update_one({"user_id": user.id}, {"$push": {
            "birthdays": {
                "day": day,
                "month": month,
                "person": person
            }
        }})

async def setup(bot):
    bot.manager = birthdays_manager(bot)