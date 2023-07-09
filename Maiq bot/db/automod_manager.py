from typing import Optional

# TODO:
# turn this and all the other mongodb things into async
# odm with mongoengine

class AutomodManager:
    def __init__(self, db):
        self.tracker = db['automod_tracker']
        self.config = db['automod_config']

    def create_record(self, guild_id, user_id):
        self.tracker.insert_one({
            'guild_id': guild_id,
            'user_id': user_id,
            'count': 1
        })

    def increment_record(self, guild_id, user_id):
        self.tracker.update_one(
            {'guild_id': guild_id, 'user_id': user_id}, 
            {'$inc': {'count': 1}}
        )

    def get_record(self, guild_id, user_id):
        return self.tracker.find_one({ 'guild_id': guild_id, 'user_id': user_id })
    
    def increment_record_and_get_count(self, guild_id, user_id):
        record = self.get_record(guild_id, user_id)

        if record is None:
            self.create_record(guild_id, user_id)
        else:
            self.increment_record(guild_id, user_id)

        return record['count'] + 1 if record is not None else 1
    
    # config stuff

    def get_config(self, server_id):
        return self.config.find_one({ 'server_id': server_id })
    
    def create_config(self, server_id, server_name, channel_id, channel_name):
        self.config.insert_one({
            'server_id': server_id,
            'server_name': server_name,
            'channel_id': channel_id,
            'channel_name': channel_name,
            'dangerous_words': [],
            'prohibited_words': [],
            'enabled': True,
        })

    def update_config_channel(self, server_id, server_name, channel_id, channel_name):
        if self.get_config(server_id) is None:
            self.create_config(server_id, server_name, channel_id, channel_name)
            return

        self.config.update_one(
            {'server_id': server_id},
            {'$set': {'channel_id': channel_id, 'channel_name': channel_name}}
        )

    def update_config_enabled(self, server_id: str, enabled: bool) -> Optional[bool]:
        if self.get_config(server_id) is None:
            return None
        
        # maybe I should instead do result = self.config... and then return it
        self.config.update_one(
            {'server_id': server_id},
            {'$set': {'enabled': enabled}}
        )
        return enabled

    def add_dangerous_word(self, server_id, word):
        self.config.update_one(
            {'server_id': server_id},
            {'$push': {'dangerous_words': word}}
        )

    def add_prohibited_word(self, server_id, word):
        self.config.update_one(
            {'server_id': server_id},
            {'$push': {'prohibited_words': word}}
        )

    def remove_dangerous_word(self, server_id, word):
        self.config.update_one(
            {'server_id': server_id},
            {'$pull': {'dangerous_words': word}}
        )

    def remove_prohibited_word(self, server_id, word):
        self.config.update_one(
            {'server_id': server_id},
            {'$pull': {'prohibited_words': word}}
        )

    def get_dangerous_words(self, server_id):
        return self.config.find_one({ 'server_id': server_id })['dangerous_words']
    
    def get_prohibited_words(self, server_id):
        return self.config.find_one({ 'server_id': server_id })['prohibited_words']
    


