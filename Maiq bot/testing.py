import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from umongo import Document, fields
from umongo.frameworks import MotorAsyncIOInstance

import os
from dotenv import load_dotenv
load_dotenv()


CONNECTION_STRING = f"mongodb+srv://RootOfMinus1:{os.getenv('MANGO')}@cluster0.ccfbwh6.mongodb.net/?retryWrites=true&w=majority"

client = AsyncIOMotorClient(CONNECTION_STRING)
db = client.CatWithHorns
instance = MotorAsyncIOInstance(db)


@instance.register
class User(Document):
    _id = fields.ObjectIdField()
    first_name = fields.StringField()
    last_name = fields.StringField()
    age = fields.IntegerField()

    class Meta:
        collection_name = "users"

    def __repr__(self):
        return f"User({self.first_name}, {self.last_name}, {self.age})"


async def motor_test():
    found_user: User = await User.find_one({"first_name": 'bingleshoe'})
    print(found_user)


async def main():
    await motor_test()


# apparently this doesn't work
asyncio.run(main())

# and you have to use this??
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

# I should check out beanie









