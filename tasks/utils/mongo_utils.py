from pymongo import MongoClient

import os

mongo_user = os.environ["MONGO_USERNAME"]
mongo_password = os.environ.get("MONGO_PASSWORD")

CONNECTION_STRING_TEMPLATE = "mongodb://{username}:{password}@mongodb:27017/youtubedb"
CONNECTION_STRING = CONNECTION_STRING_TEMPLATE.format(
    username = mongo_user,
    password = mongo_password
)

mongo_client = MongoClient(CONNECTION_STRING)

def get_db():
    """Returns the youtube database"""
    return mongo_client['youtubedb']

def get_configs():
    """Returns the configs collection."""
    db = get_db()
    configs = db.configs
    config = configs.find_one({}, sort=[( '_id', -1 )])

    if config is None:
        raise Exception("No configs found !")
    
    return config

def get_api_keys():
    """Returns the youtube api keys stored."""
    config = get_configs()
    return config['tokens']
