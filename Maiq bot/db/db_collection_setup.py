from pymongo import MongoClient, ASCENDING, IndexModel
import os
from dotenv import load_dotenv
load_dotenv()

CONNECTION_STRING = f"mongodb+srv://RootOfMinus1:{os.getenv('MANGO')}@cluster0.ccfbwh6.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client.get_database('CatWithHorns')


def change_expiration_time(db, collection, time):
    db.runCommand({
        "collMod": collection,  # your collection name
        "index": {
            "keyPattern": {"expires_at": 1},
            "expireAfterSeconds": time
        }
    })
    print(f"Expiration time updated to {time} seconds")

# change_expiration_time(db, "warnings_v2", timedelta(days=90).total_seconds())



def create_expiration_time(db, collection, time):
    db[collection].create_index("expires_at", time)
    print(f"Index for {db}.{collection} created successfully ({time}).")

# create_expiration_time(db, "warnings_v2", timedelta(days=90).total_seconds())


