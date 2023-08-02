import discord
from discord.ext import commands
from pymongo import ASCENDING, DESCENDING

class another_manager:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.collection = self.bot.db['serious_birthdays']
        self.config = self.bot.db['serious_birthdays_config']

    def create_config_server(self, server: discord.Guild, channel: discord.TextChannel):
        self.config.insert_one({
            "server_id": server.id,
            "server_name": server.name,
            "channel_id": channel.id,
            "channel_name": channel.name,
            "time": 8,
            "timezone": "uhh UTC or something idk how to keep track of that yet",
            "birthdays": []
        })

    def find_birthdays_for_time(self, hour: int):
        pass


class birthdays_manager:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.collection = self.bot.db['serious_birthdays']
        self.config = self.bot.db['serious_birthdays_config']

    def add_birthday(self, person: str, day: int, month: int, server: discord.Guild, dm_user: discord.User):
        # could be used in another manager
        """
        if server:
            self.config.update_one({
                "server_id": server.id
            }, {
                "$push": {
                    "birthdays": {
                        "person": person,
                        "day": day,
                        "month": month
                    }
                }
            })
        """

        if server:
            server_id = server.id
            server_name = server.name
            dm_user_id = None
            dm_user_name = None
        else:
            server_id = None
            server_name = None
            dm_user_id = dm_user.id
            dm_user_name = dm_user.name

        self.collection.insert_one({
            "person": person,
            "day": day,
            "month": month,
            "server_id": server_id,
            "server_name": server_name,
            "dm_id": dm_user_id,
            "dm_name": dm_user_name
        })
    
    def get_birthdays(self, server: discord.Guild, dm_user: discord.User):
        if server:
            birthdays =  self.collection.find({
            "server_id": server.id
            })
        else:
            birthdays =  self.collection.find({
            "dm_id": dm_user.id
            })

        birthdays.sort([("month", ASCENDING), ("day", ASCENDING)])

        return birthdays

    def create_config(self, server: discord.Guild, channel: discord.TextChannel, dm_user: discord.User):
        if server:
            server_id = server.id
            server_name = server.name
            channel_id = channel.id
            channel_name = channel.name
            dm_user_id = None
            dm_user_name = None
        else:
            server_id = None
            server_name = None
            channel_id = None
            channel_name = None
            dm_user_id = dm_user.id
            dm_user_name = dm_user.name

        chunk = {
            "server_id": server_id,
            "server_name": server_name,
            "channel_id": channel_id,
            "channel_name": channel_name,
            "dm_id": dm_user_id,
            "dm_name": dm_user_name,
            "time": 8,
            "timezone": "uhh UTC or something idk how to keep track of that yet",
        }

        self.config.insert_one(chunk)

        return chunk

    def get_configs_for_hour(self, hour: int):
        return self.config.find({
            "time": hour
        })
    
    def get_config(self, server: discord.Guild, dm_user: discord.User):
        if server:
            return self.config.find_one({
                "server_id": server.id
            })
        else:
            return self.config.find_one({
                "dm_id": dm_user.id
            })