from pymongo import MongoClient
from decouple import config

client = MongoClient(config('DATABASE_URI'))

db = client.portfolio