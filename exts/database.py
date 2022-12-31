from pymongo import MongoClient

from tokens import MONGODB_URL

cluster = MongoClient(MONGODB_URL)

db = cluster['uncledunk']
economy_collection = db['economy']
settings_collection = db['settings']