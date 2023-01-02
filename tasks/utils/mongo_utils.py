import os
import dateutil.parser

from pymongo import MongoClient, errors

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

def load_into_db(videos):
    """Store the api response in the db."""
    if len(videos) == 0:
        return
    
    # Parsing the date into a datetime object
    for video in videos:
        published_time = video['snippet']['publishTime']
        video['publishTime'] = dateutil.parser.isoparse(published_time)

    db = get_db()

    try:
        db.youtube_videos.insert_many(videos, ordered=False)
    except errors.BulkWriteError as e:
        e.details['writeErrors']
        exceptions = []

        for x in e.details['writeErrors']:
            # 11000 code is for duplicates, we dont want to raise exception if duplicate is found
            if x['code'] != 11000:
                exceptions.append(x)

        if len(exceptions) > 0:
            print("Something went wrong while inserting in mongodb.", exceptions)
