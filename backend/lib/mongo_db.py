# from flask_mongoengine import MongoEngine
from pymongo import MongoClient

from lib.config import env

# db = MongoEngine()

cluster = MongoClient(host=env.DB_HOST, port=int(env.DB_PORT))
db = cluster[env.DB_NAME]


