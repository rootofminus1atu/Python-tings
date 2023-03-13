"""import gspread

oc_info = {
    "Luki": {
        "emoji": "<:luki_oc:1059974898346381402>",
        "short_description": "The main goober of the gang!",

        "description": "he has horns",
        "side_color": "0x397fbf",  # remember to change the # to 0x (for example #72bae0 -> 0x72bae0)
        "created_by": "@Luki#8233",
        "created_on": "Current design - about September 2022 (Oc was made even in like 2013 itself)",
        "image": "https://cdn.discordapp.com/attachments/826727568798384151/1059145409240514680/horny_cat_reference.png"
    },
    "Silver": {
        "emoji": "<:silver_oc:1060693133110808581>",
        "short_description": "2nd goober, thats why she's silver!",

        "description": "She is my second main oc, but not one of the first i got. He is the goofy computer nerd too (this is why he has programming sock lol)",
        "side_color": "0xd290e0",
        "created_by": "@Luki#8233 (adopted from Lefi#9262 in fta oc adopts)",
        "created_on": "10th May 2020",
        "image": "https://cdn.discordapp.com/attachments/1050804339536564315/1060692159466053762/fake_horny_cat_ref.png"
    },
    "Enikő": {
        "emoji": "<:eniko_oc:1059974924468490383>",
        "short_description": "The cat that can glow!",

        "description": "magyar oc!",
        "side_color": "0xf829ff",
        "created_by": "@Luki#8233",
        "created_on": "24th August 2022",
        "image": "https://cdn.discordapp.com/attachments/1020620787289423892/1059787608697339984/Untitled620_20230103115610.png"
    },
    "Darky": {
        "emoji": "<:darky_oc:1064154534018035794>",
        "short_description": "The Goofy and dumb, red fluffy goober!",

        "description": "Even if he is big, and look really dangerous, he actually wouldn't even hurt a fly, he is so dumb for it. Actually really dumb and goofy goober.",
        "side_color": "0x992222",
        "created_by": "@Luki#8233 (adopted from Lefi#9262 in fta oc adopts)",
        "created_on": "19th May 2020",
        "image": "https://cdn.discordapp.com/attachments/1020620787289423892/1064166769553584198/the_more_horny_cat_oc_ref.png"
    },
    "Roxy": {
        "emoji": "<:roxy_oc:1063385384123379764>",
        "short_description": "She is not from the Minefield!",

        "description": "She is really goofy goober cat, even if she doesn't has like arm and leg she is really silly and goofy :blehh:",
        "side_color": "0x32c971",
        "created_by": "@Luki#8233 (adopted from Lefi#9262 in fta oc adopts)",
        "created_on": "12th May 2020",
        "image":
"https://cdn.discordapp.com/attachments/1020620787289423892/1063580064282841108/the_her_oc_ref.png"
    },
    "Lefhor": {
        "emoji": "<:lefhor_oc:1067042129668489237>",
        "short_description": "Actual amalgamation of 2 ocs!",

        "description": "The silly looking, catlover928282 (normal internet username), he is silly and can fly, tbh idk what i can add more to him other that he was actually made out of 2 oc's",
        "side_color": "0x858dc9",
        "created_by": "@Lefi#9262 (Adopted by @Luki#8233 in 17th July 2020)",
        "created_on": "15 April 2020",
        "image":
"https://cdn.discordapp.com/attachments/1020620787289423892/1067164210389336124/silly_horny_cat_ref.png"
    },
    "Charles": {
        "emoji": "<:charles_oc:1069747345077575690>",
        "short_description": "Charles - Local emo oc, with kinda chad design.",

        "description": "I'm too lazy to write it, im sorry!",
        "side_color": "0xf5b942",
        "created_by": "@Lefi#9262 (Adopted by @Luki#8233 in 18th November 2020)",
        "created_on": "About 2019. Exact date unknown.",
        "image":
"https://cdn.discordapp.com/attachments/1020620787289423892/1069747256242229368/the_least_main_goober.png"
    },
    "Snow": {
        "emoji": "<:snow_oc:1071573546364584037>",
        "short_description": "Snow - 4 eyes, 2 tails. - Coolest looking oc!",

        "description": "Oops, my creator forgot to write a description... - Suka Blyat",
        "side_color": "0x919fcf",
        "created_by": "@Lefi#9262 (Adopted by @Luki#8233 in 17th July 2020)",
        "created_on": "17th July 2020",
        "image":
"https://cdn.discordapp.com/attachments/1020620787289423892/1071568176288108604/the_double_horny_cat.png"
    },
}

sa = gspread.service_account(filename="catwithhorns-fe460388a5f0.json")
sh = sa.open("Testing")

wks = sh.worksheet("oc_info")

print(wks.get_all_records())




headers = ['name'] + list(oc_info["Luki"].keys())
rows = [[k] + list(v.values()) for k, v in oc_info.items()]

values = [headers] + rows




# wks.update("A1", values)



# print(wks.acell('A3').value)
# print(wks.cell(3, 2).value)
# print(wks.get("A1:C4"))

# wks.update('A3', 'Eniko')

# wks.update('F2', '=UPPER(A4)', raw=False)"""


from pymongo import MongoClient, ASCENDING, IndexModel
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()

"""  # BAD
try:
    data.drop_index("expiration_time")
except:
    pass
index = IndexModel([("expires_at", ASCENDING)], expireAfterSeconds=int(expiration_time.total_seconds()), name="expiration_time")
data.create_indexes([index])
"""

"""expiration_time = timedelta(seconds=60)
print(int(expiration_time.total_seconds()))"""




CONNECTION_STRING = f"mongodb+srv://RootOfMinus1:{os.getenv('MANGO')}@cluster0.ccfbwh6.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)

db = client.get_database('CatWithHorns')
warnings = db.warnings

print(warnings.count_documents({}))


def change_expiration_time(time):
    db.command({
        "collMod": "warnings",
        "index": {
            "keyPattern": {"expires_at": 1},
            "expireAfterSeconds": time
        }
    })
    print(f"Expiration time updated to {time} seconds")

# change_expiration_time(timedelta(days=90).total_seconds())


def get_ttl(collection):  # ttl = time to live
    default = timedelta(days=90)  # the default expiration time, DO NOT change it

    indexes = collection.list_indexes()
    for index in indexes:
        if 'expireAfterSeconds' in index:
            return index['expireAfterSeconds']
    return default

def add_warn(user_id, reason, level, warned_by):
    rn = datetime.now()
    warn_data = {
        "user_id": str(user_id),
        "reason": str(reason),
        "warn_level": int(level),
        "warned_by": str(warned_by),
        "created_at": rn,
    }
    warnings.insert_one(warn_data)


def get_warns(user_id):
    results = warnings.find({"user_id": str(user_id)})
    return list(results)


def delete_warn(_id):
    warnings.delete_one({"_id": ObjectId(_id)})

