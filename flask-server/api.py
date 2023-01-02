import json
import os
from flask import Flask, jsonify
from pymongo import MongoClient, DESCENDING
from bson import json_util

app = Flask(__name__)

mongo_user = os.environ["MONGO_USERNAME"]
mongo_password = os.environ.get("MONGO_PASSWORD")

CONNECTION_STRING_TEMPLATE = "mongodb://{username}:{password}@mongodb:27017/youtubedb"
CONNECTION_STRING = CONNECTION_STRING_TEMPLATE.format(
    username = mongo_user,
    password = mongo_password
)

# Connect to the mongodb
mongo_client = MongoClient(CONNECTION_STRING)

# Get the youtubeDB, and the youtube_videos collection
db = mongo_client['youtubedb']
youtube_videos = db["youtube_videos"]

DEFAULT_PAGE_LIMIT = '5'
MAX_PAGE_LIMIT = 50
API_URL = 'http://localhost:8000/get?page={page}&limit={limit}'

@app.route('/get', methods=['GET'])
def get_videos():
    """Endpoint to retrieve all of the youtube data in a paginated form."""
    videos = youtube_videos.find()
    videos = videos.sort('snippet.publishTime', DESCENDING)
    videos = videos.limit(5)

    res = {
        'results': list(json.loads(json_util.dumps(videos)))
    }

    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)