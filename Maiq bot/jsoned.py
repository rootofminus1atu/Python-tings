from pymongo import MongoClient, ASCENDING, IndexModel
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import time
from testing import *
import os
from dotenv import load_dotenv
load_dotenv()

CONNECTION_STRING = f"mongodb+srv://RootOfMinus1:{os.getenv('MANGO')}@cluster0.ccfbwh6.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)

db = client.get_database('CatWithHorns')
warnings = db.warnings


change_expiration_time(timedelta(days=90).total_seconds())
