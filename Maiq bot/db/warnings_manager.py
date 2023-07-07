from datetime import datetime, timedelta
from bson.objectid import ObjectId, InvalidId
from pymongo import DESCENDING


class WarningsManager:
    def __init__(self, db):
        self.collection = db['warnings_v2']

    def add_warning(self, warning):
        warning_data = warning.to_dict()
        result = self.collection.insert_one(warning_data)
        warning._id = result.inserted_id  # Update _id of the Warning object

    def get_warnings(self, user_id, server_id):
        query = {"user_id": str(user_id), "server_id": str(server_id)}
        results = self.collection.find(query).sort("created_at", DESCENDING)
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
            return f"Deleted warning with id `{warning_id}` for user {found_warning.user_name}"

    def try_get_warning(self, warning_id, server_id):
        try:
            warning_id = ObjectId(warning_id)
        except (InvalidId, TypeError):
            return None

        return self.collection.find_one({"_id": warning_id, "server_id": str(server_id)})

    def delete_warning(self, warning):
        self.collection.delete_one({"_id": warning._id})

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
    def __init__(self, user_id, user_name, level, reason, mod_id, mod_name, server_id, server_name, created_at: datetime):
        self._id = None  # Initialize _id as None by default
        self.user_id = str(user_id)
        self.user_name = str(user_name)
        self.level = int(level)
        self.reason = str(reason)
        self.mod_id = str(mod_id)
        self.mod_name = str(mod_name)
        self.server_id = str(server_id)
        self.server_name = str(server_name)
        self.created_at: datetime = created_at

    def to_dict(self):
        data = {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "level": self.level,
            "reason": self.reason,
            "mod_id": self.mod_id,
            "mod_name": self.mod_name,
            "server_id": self.server_id,
            "server_name": self.server_name,
            "created_at": self.created_at
        }
        if self._id:
            data["_id"] = self._id
        return data

    @classmethod
    def from_dict(cls, data):
        warning = cls(
            data["user_id"],
            data["user_name"],
            data["level"],
            data["reason"],
            data["mod_id"],
            data["mod_name"],
            data["server_id"],
            data["server_name"],
            data["created_at"]
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