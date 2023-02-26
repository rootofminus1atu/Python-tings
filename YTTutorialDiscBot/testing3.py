from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv


# database testing and learning


load_dotenv()

CONNECTION_STRING = f"mongodb+srv://RootOfMinus1:{os.getenv('MANGO')}@cluster0.wwryc2o.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)

db = client.get_database('addibot_db')
data = db.addibot_data

print(data.count_documents({}))
print(data.find_one())
#data.update_one({}, {'$set': {'activity': 'off'}})
print(data.find_one())


db = client.get_database('catbot_db')
test = db.test

quote_translation = {
    "Papiez": "Pope",
    "Tak": "Yes",
    "Tak jak pan Jezus powiedział": "Just like the Lord Jesus said"
}
test.insert_one(quote_translation)
