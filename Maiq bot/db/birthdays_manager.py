

class BirthdaysManager:
    def __init__(self, db):
        self.collection = db['birthdays']

    def add_birthday(self, guild_id, name, day, month):
        self.collection.insert_one({
            'guild_id': guild_id,
            'name': name,
            'day': day,
            'month': month
        })

    def get_birthdays_for_date(self, day, month):
        cursor = self.collection.find({
            'day': day,
            'month': month
        })
        birthdays = list(cursor)
        return birthdays
    
    def get_birthday_servers(self):
        return self.collection.distinct('guild_id')