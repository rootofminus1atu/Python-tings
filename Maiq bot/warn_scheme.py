from datetime import datetime, timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
import os
from dotenv import load_dotenv
load_dotenv()

CONNECTION_STRING = f"mongodb+srv://RootOfMinus1:{os.getenv('MANGO')}@cluster0.ccfbwh6.mongodb.net/?retryWrites=true&w=majority"

class WarningsManager:
    def __init__(self):
        self.client = MongoClient(CONNECTION_STRING)
        self.db = self.client.get_database('CatWithHorns')
        self.collection = self.db['warnings_v2']

    def add_warning(self, warning):
        warning_data = warning.to_dict()
        result = self.collection.insert_one(warning_data)
        warning._id = result.inserted_id  # Update _id of the Warning object

    def get_warnings(self, user_id, server_id):
        query = {"user_id": str(user_id), "server_id": str(server_id)}
        results = self.collection.find(query)
        return [Warning.from_dict(data) for data in results]
    
    def try_delete_warning(self, warning_id, server_id):
        try:
            warning_id = ObjectId(warning_id)
        except (InvalidId, TypeError):
            return f"Invalid warning id: `{warning_id}`"
        
        found_warning = self.collection.find_one({"_id": warning_id, "server_id": str(server_id)})
        
        if found_warning is None:
            return f"Warning with id `{warning_id}` not found."
        else:
            self.collection.delete_one({"_id": warning_id})
            return f"Deleted warning with id `{warning_id}`"
        
    def get_ttl(self):  # ttl = time to live
        """
        Retrieves the Time To Live (ttl) value in SECONDS.
        """
        default = timedelta(days=90)  # the default expiration time, DO NOT change it

        indexes = self.collection.list_indexes()
        for index in indexes:
            if 'expireAfterSeconds' in index:
                return index['expireAfterSeconds']
        return default


class Warning:
    def __init__(self, user_id, user_name, level, reason, mod_id, mod_name, server_id, server_name, created_at):
        self._id = None  # Initialize _id as None by default
        self.user_id = str(user_id)
        self.user_name = str(user_name)
        self.level = int(level)
        self.reason = str(reason)
        self.mod_id = str(mod_id)
        self.mod_name = str(mod_name)
        self.server_id = str(server_id)
        self.server_name = str(server_name)
        self.created_at = created_at

    def to_dict(self):
        return {
            "_id": self._id,  # Include _id in the dictionary
            "user_id": self.user_id,
            "user_name": self.user_name,
            "level": self.level,
            "reason": self.reason,
            "mod_id": self.mod_id,
            "mod_name": self.mod_name,
            "server_id": self.server_id,
            "server_name": self.server_name,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        created_at = datetime.fromisoformat(data["created_at"])
        warning = cls(
            data["user_id"],
            data["user_name"],
            data["level"],
            data["reason"],
            data["mod_id"],
            data["mod_name"],
            data["server_id"],
            data["server_name"],
            created_at=created_at
        )
        warning._id = data.get("_id")  # Set _id if present in the data
        return warning

class WarnLevel:
    def __init__(self, emoji, color, name):
        self.emoji = emoji
        self.color = color
        self.name = name

warn_levels = {
    0: WarnLevel("🔵", 0x55ACEE, "Verbal"),
    1: WarnLevel("🟢", 0x78B159, "Normal"),
    3: WarnLevel("🟡", 0xFDCB58, "Medium"),
    5: WarnLevel("🟠", 0xF4900C, "Big"),
    7: WarnLevel("🔴", 0xDD2E44, "Huge"),
    10: WarnLevel("⚫", 0x000000, "nil")
}   

        

"""


client = MongoClient(CONNECTION_STRING)

db = client.get_database('CatWithHorns')
warnings = db.warnings



# DB MANIPULATION HELPER FUNCTIONS
# currently this whole db thing is a mess
# in the future I'd like to restructure all that into something more oop-like
# and most (if not all) db related code could be kept in a separate file


def add_warn(user_id, reason, level, mod_id, server_id):
    rn = datetime.now()
    warn_data = {
        "user_id": str(user_id),
        "mod_id": str(mod_id),
        "server_id": str(server_id),
        "warn_level": int(level),
        "reason": str(reason),
        "created_at": rn,
    }
    warnings.insert_one(warn_data)


def get_warns(user_id, server_id):
    results = warnings.find({"user_id": str(user_id), "server_id": str(server_id)})
    return list(results)

def get_all_warns(user_id):
    results = warnings.find({"user_id": str(user_id)})
    return list(results)

"""