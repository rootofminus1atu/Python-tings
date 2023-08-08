import discord
from discord.ext import commands
from typing import Optional, Tuple, Dict, List, Union
import timeit

DEFAULT_TIME = 8
DEFAULT_TIMEZONE = "UTC"

class MyGuild(discord.Guild):
    def __init__(self, id, name):
        self.id = id
        self.name = name

class MyUser():
    def __init__(self, id, name):
        self.id = id
        self.name = name

class MyBot(commands.Bot):
    def __init__(self, name):
        self.name = name

class MyInteraction():
    def __init__(self, guild, channel, user):
        self.guild = guild
        self.channel = channel
        self.user = user

class MyChannel(discord.TextChannel):
    def __init__(self, id, name):
        self.id = id
        self.name = name



class BaseManager:
    def __init__(self, bot: commands.Bot, collection: str):
        self.bot = bot
        # self.collection = self.bot.db[collection]
        self.collection = collection

class BirthdaysManagerMotor(BaseManager):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot, collection="birthdays-col")

    def interaction_type_filter(interaction: MyInteraction) -> Dict[str, int]:
        """
        Returns:
            - `{"server_id": interaction.guild.id}` in the case of a server interaction
            - `{"user_id": interaction.user.id}` in the case of a user interaction
        """
        if interaction.guild:
            return {"server_id": interaction.guild.id}
        else:
            return {"user_id": interaction.user.id}
            
        

    async def create_config(self, interaction: MyInteraction, and_birthday=None, time=DEFAULT_TIME, timezone=DEFAULT_TIMEZONE) -> None:
        server_or_user = self.interaction_type_filter(interaction)

        new_config = {
            **server_or_user,
            "time": time,
            "timezone": timezone,
            "birthdays": [] if and_birthday is None else [and_birthday]
        }

        if interaction.guild:
            new_config["channel_id"] = interaction.channel.id

        await self.collection.insert_one(new_config)

    async def get_config(self, interaction: MyInteraction) -> Optional[Dict]:
        server_or_user = self.interaction_type_filter(interaction)

        return await self.collection.find_one(server_or_user)
        
    async def get_config_from_person_birthday(self, interaction: MyInteraction, person: str) -> Optional[Dict]:
        server_or_user = self.interaction_type_filter(interaction)

        return await self.collection.find_one({
            **server_or_user,
            "birthdays": {"$elemMatch": {"person": person}}
            })
    
    async def update_config_channel(self, interaction: MyInteraction, channel: MyChannel) -> None:
        if interaction.guild is None:
            return

        server_or_user = self.interaction_type_filter(interaction)

        await self.collection.update_one(
            server_or_user, 
            {"$set": {"channel_id": channel.id}})

    async def update_config_time(self, interaction: MyInteraction, time: int, timezone: str) -> None:
        server_or_user = self.interaction_type_filter(interaction)

        await self.collection.update_one(
            server_or_user, 
            {"$set": {"time": time, "timezone": timezone}})
        
    async def add_birthday(self, interaction: MyInteraction, birthday: Dict) -> None:
        server_or_user = self.interaction_type_filter(interaction)

        await self.collection.update_one(
            server_or_user, 
            {"$push": {"birthdays": birthday}})
        
    async def remove_birthday(self, interaction: MyInteraction, person: str) -> None:
        server_or_user = self.interaction_type_filter(interaction)

        await self.collection.update_one(
            server_or_user, 
            {"$pull": {"birthdays": {"person": person}}})
        
    async def get_birthdays(self, interaction: MyInteraction) -> Optional[List[Dict]]:
        server_or_user = self.interaction_type_filter(interaction)

        config = await self.collection.find_one(server_or_user)
        if config is None:
            return None

        return config["birthdays"]
    
    async def add_birthday_if_not_exist(self, interaction: MyInteraction, birthday: Dict) -> None:
        server_or_user = self.interaction_type_filter(interaction)

        cursor = self.collection.find({
            **server_or_user,
            "birthdays": {"$elemMatch": {"person": birthday["person"]}}
            })
        
        if cursor.count() == 0:
            pass
            # WIP



from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import tzdata

def time_thing(hour: int, timzon: str):
    rn = datetime.now(ZoneInfo("UTC"))
    dt = rn.replace(hour=hour, tzinfo=ZoneInfo(timzon))

    print(rn)
    print(dt)
    print(rn == dt)
    return rn == dt

time_thing(19, "Poland")

hours = [i for i in range(24)]
tzs = {
    "UTC+0": {
        "a": ""
    }
}

def add_time(hour: int, timzon: str, dst: bool):
    pass

    
