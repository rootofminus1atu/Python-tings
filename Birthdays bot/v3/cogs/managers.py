import discord
from discord.ext import commands
from colorama import Fore
from typing import Optional, Tuple, Union, Dict, List
from datetime import datetime, timezone
import pytz
import zoneinfo
import tzdata


SituationType = Tuple[Union[discord.Guild, discord.User], Optional[discord.TextChannel]]

class TestingManager:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.collection = self.bot.db['testing']
        self.collection_another = self.bot.db['testing_filtering']

    def create_time(self, hour, timezone_name):
        target_date = datetime(2000, 1, 1, hour, 0, 0, 0, tzinfo=pytz.utc)
        target_time = target_date.astimezone(pytz.timezone(timezone_name)).isoformat()

        print(target_time)

        self.collection.insert_one({
            "name": "jeff",
            "hour": hour,
            "timezone": timezone,
            "target_time": target_time
        })

    def filtering_thing(self, date: datetime):
        result = self.collection_another.aggregate([
            {
                "$match": {
                    "time": date.hour,
                    "birthdays": {
                        "$elemMatch": {
                            "day": date.day,
                            "month": date.month
                        }
                    }
                }
            },
            {
                "$addFields": {
                    "birthdays": {
                        "$filter": {
                            "input": "$birthdays",
                            "as": "birthday",
                            "cond": {
                                "$and": [
                                    { "$eq": ["$$birthday.day", date.day] },
                                    { "$eq": ["$$birthday.month", date.month] }
                                ]
                            }
                        }
                    }
                }
            }
        ])
        result_list = list(result)
        return result_list

DEFAULT_TIME = 8
DEFAULT_TIMEZONE = "UTC"

class BaseManager:
    def __init__(self, bot: commands.Bot, collection: str):
        self.bot = bot
        self.collection = self.bot.db[collection]

# NOTE:
# I could use dispatchers and reducers to make this more efficient (look at react)

class BirthdaysManagerMotor(BaseManager):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot, collection="serious_birthdays_config")

    async def create_config(self, situation: SituationType, and_birthday=None, time=DEFAULT_TIME, timezone=DEFAULT_TIMEZONE):
        place, channel = situation

        # if channel === if we're in a server
        if channel:
            config = {
                "server_id": place.id,
                "server_name": place.name,
                "channel_id": channel.id,
                "channel_name": channel.name
            }
        else:
            config = {
                "user_id": place.id,
                "user_name": place.name
            }
        
        config.update({
            "time": time,
            "timezone": timezone,
            "birthdays": []
        })

        if and_birthday:
            config["birthdays"].append(and_birthday)

        await self.collection.insert_one(config)
        return config
    
    async def get_config(self, situation: SituationType):
        place, channel = situation

        if channel:
            return await self.collection.find_one({"server_id": place.id})
        else:
            return await self.collection.find_one({"user_id": place.id})
        
    async def get_config_from_person_birthday(self, situation: SituationType, person: str) -> Optional[Dict]:
        place, channel = situation

        if channel:
            return await self.collection.find_one({"server_id": place.id, "birthdays": {"$elemMatch": {"person": person}}})
        else:
            return await self.collection.find_one({"user_id": place.id, "birthdays": {"$elemMatch": {"person": person}}})
    
    async def update_config_channel(self, situation: SituationType, target_channel: discord.TextChannel):
        place, channel = situation

        if not channel:
            return

        await self.collection.update_one({"server_id": place.id}, {"$set": {
            "channel_id": target_channel.id,
            "channel_name": target_channel.name
        }})

    async def update_config_time(self, situation: SituationType, time: int, timezone: str):
        place, channel = situation

        if channel:
            await self.collection.update_one({"server_id": place.id}, {"$set": {
                "time": time,
                "timezone": timezone
            }})
        else:
            await self.collection.update_one({"user_id": place.id}, {"$set": {
                "time": time,
                "timezone": timezone
            }})

    async def add_birthday(self, situation: SituationType, birthday: dict):
        place, channel = situation

        if channel:
            await self.collection.update_one({"server_id": place.id}, {"$push": {"birthdays": birthday}})
        else:
            await self.collection.update_one({"user_id": place.id}, {"$push": {"birthdays": birthday}})


    async def get_birthdays(self, situation: SituationType) -> Optional[List]:
        config = await self.get_config(situation)

        if not config:
            return None

        birthdays = config.get("birthdays", [])

        sorted_birthdays = sorted(birthdays, key=lambda bday: (bday["month"], bday["day"]))

        return sorted_birthdays
    
    async def get_birthday_from_person(self, situation: SituationType, person: str) -> Optional[list]:
        config = await self.get_config(situation)

        if not config:
            return None
        
        birthdays = config["birthdays"]

        for birthday in birthdays:
            if birthday["person"] == person:
                return birthday
        
        return None
    
    async def remove_birthday(self, situation: SituationType, person: str):
        place, channel = situation

        if channel:
            await self.collection.update_one({"server_id": place.id}, {"$pull": {"birthdays": {"person": person}}})
        else:
            await self.collection.update_one({"user_id": place.id}, {"$pull": {"birthdays": {"person": person}}})

    async def get_configs_with_birthdays_for_datetime(self, date: datetime):
        # this could definitely use more async stuff

        result = await self.collection.aggregate([
            {
                "$match": {
                    "time": date.hour,
                    "birthdays": {
                        "$elemMatch": {
                            "day": date.day,
                            "month": date.month
                        }
                    }
                }
            },
            {
                "$addFields": {
                    "birthdays": {
                        "$filter": {
                            "input": "$birthdays",
                            "as": "birthday",
                            "cond": {
                                "$and": [
                                    { "$eq": ["$$birthday.day", date.day] },
                                    { "$eq": ["$$birthday.month", date.month] }
                                ]
                            }
                        }
                    }
                }
            }
        ]).to_list(length=None)

        return result


class BirthdaysManager(BaseManager):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot, collection="serious_birthdays_config")

    def create_config(self, situation: SituationType, and_birthday=None, time=DEFAULT_TIME, timezone=DEFAULT_TIMEZONE):
        place, channel = situation

        # if channel === if we're in a server
        if channel:
            config = {
                "server_id": place.id,
                "server_name": place.name,
                "channel_id": channel.id,
                "channel_name": channel.name
            }
        else:
            config = {
                "user_id": place.id,
                "user_name": place.name
            }
        
        config.update({
            "time": time,
            "timezone": timezone,
            "birthdays": []
        })

        if and_birthday:
            config["birthdays"].append(and_birthday)

        self.collection.insert_one(config)
        return config

    def get_config(self, situation: SituationType) -> Optional[dict]:
        place, channel = situation

        if channel:
            return self.collection.find_one({"server_id": place.id})
        else:
            return self.collection.find_one({"user_id": place.id})

    def get_config_from_person_birthday(self, situation: SituationType, person: str) -> Optional[dict]:
        place, channel = situation

        if channel:
            return self.collection.find_one({"server_id": place.id, "birthdays": {"$elemMatch": {"person": person}}})
        else:
            return self.collection.find_one({"user_id": place.id, "birthdays": {"$elemMatch": {"person": person}}})

    # or maybe using a few more classes would've been better
    def update_config_channel(self, situation: SituationType, target_channel: discord.TextChannel):
        place, channel = situation

        if not channel:
            return

        self.collection.update_one({"server_id": place.id}, {"$set": {
            "channel_id": target_channel.id,
            "channel_name": target_channel.name
        }})

    def update_config_time(self, situation: SituationType, time: int, timezone: str):
        place, channel = situation

        if channel:
            self.collection.update_one({"server_id": place.id}, {"$set": {
                "time": time,
                "timezone": timezone
            }})
        else:
            self.collection.update_one({"user_id": place.id}, {"$set": {
                "time": time,
                "timezone": timezone
            }})

    def add_birthday(self, situation: SituationType, birthday: dict):
        place, channel = situation

        if channel:
            self.collection.update_one({"server_id": place.id}, {"$push": {"birthdays": birthday}})
        else:
            self.collection.update_one({"user_id": place.id}, {"$push": {"birthdays": birthday}})
    
    def get_birthdays(self, situation: SituationType) -> Optional[list]:
        config = self.get_config(situation)

        if not config:
            return None
        
        birthdays = config["birthdays"]

        sorted_birthdays = sorted(birthdays, key=lambda bday: (bday["month"], bday["day"]))

        return sorted_birthdays
    
    def get_birthday_from_person(self, situation: SituationType, person: str) -> Optional[list]:
        config = self.get_config(situation)

        if not config:
            return None
        
        birthdays = config["birthdays"]

        for birthday in birthdays:
            if birthday["person"] == person:
                return birthday
        
        return None
    
    def remove_birthday(self, situation: SituationType, person: str):
        place, channel = situation

        if channel:
            self.collection.update_one({"server_id": place.id}, {"$pull": {"birthdays": {"person": person}}})
        else:
            self.collection.update_one({"user_id": place.id}, {"$pull": {"birthdays": {"person": person}}})
    
    def get_configs_with_birthdays_for_datetime(self, date: datetime):
        result = self.collection.aggregate([
            {
                "$match": {
                    "time": date.hour,
                    "birthdays": {
                        "$elemMatch": {
                            "day": date.day,
                            "month": date.month
                        }
                    }
                }
            },
            {
                "$addFields": {
                    "birthdays": {
                        "$filter": {
                            "input": "$birthdays",
                            "as": "birthday",
                            "cond": {
                                "$and": [
                                    { "$eq": ["$$birthday.day", date.day] },
                                    { "$eq": ["$$birthday.month", date.month] }
                                ]
                            }
                        }
                    }
                }
            }
        ])
        result_list = list(result)
        return result_list
    

class Helpers:
    def get_situation(self, interaction: discord.Interaction):
        # either server
        server = interaction.guild
        channel = interaction.channel
        # or dm
        user = interaction.user

        if server:
            return (server, channel)
        else:
            return (user, None)
        
    def fancy_datetime(self, date: datetime):
        return date.strftime("%d/%m/%Y %H:%M UTC")

async def setup(bot):
    bot.manager = BirthdaysManagerMotor(bot)
    bot.helpers = Helpers()
    bot.testing = TestingManager(bot)