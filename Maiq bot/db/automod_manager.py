class AutomodManager:
    def __init__(self, db):
        self.collection = db['automod_tracker']

    def create_record(self, guild_id, user_id):
        self.collection.insert_one({
            'guild_id': guild_id,
            'user_id': user_id,
            'count': 1
        })

    def increment_record(self, guild_id, user_id):
        self.collection.update_one(
            {'guild_id': guild_id, 'user_id': user_id}, 
            {'$inc': {'count': 1}}
        )

    def get_record(self, guild_id, user_id):
        return self.collection.find_one({ 'guild_id': guild_id, 'user_id': user_id })
    
    def manage_increment_and_get_count(self, guild_id, user_id):
        record = self.get_record(guild_id, user_id)

        if record is None:
            self.create_record(guild_id, user_id)
        else:
            self.increment_record(guild_id, user_id)

        return record['count'] + 1 if record is not None else 1
