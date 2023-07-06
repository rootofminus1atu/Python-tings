from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

from db.birthdays_manager import BirthdaysManager
from db.warnings_manager import WarningsManager

CONNECTION_STRING = f"mongodb+srv://RootOfMinus1:{os.getenv('MANGO')}@cluster0.ccfbwh6.mongodb.net/?retryWrites=true&w=majority"

class DbManager:
    def __init__(self):
        self.client = MongoClient(CONNECTION_STRING)
        self.db = self.client.get_database('CatWithHorns')
        self.warnings_manager = WarningsManager(self.db)
        self.birthdays_manager = BirthdaysManager(self.db)

    def get_status(self):
        return self.client.server_info()

    