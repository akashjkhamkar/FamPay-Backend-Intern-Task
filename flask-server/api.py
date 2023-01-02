import json
import os
import dateutil.parser
import sys

from flask import Flask, jsonify, request
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

def parse_date(date):
    if date == '':
        return None

    return dateutil.parser.isoparse(date)

@app.route('/get', methods=['GET'])
def get_videos():
    """Endpoint to retrieve all of the youtube data in a paginated form."""
    args = request.args

    # Validating all the parameters
    page = args.get('page', default='1')
    page_limit = args.get('limit', default=DEFAULT_PAGE_LIMIT)
    
    if not page.isnumeric():
        return jsonify({'error': 'Invalid page.'}), 400
    
    if not page_limit.isnumeric() or int(page_limit) > MAX_PAGE_LIMIT:
        return jsonify({'error': 'Invalid page limit, page limit should be between 1 - 50 (inclusive).'}), 400
    
    page = int(page)
    page_limit = int(page_limit)

    # Check if filters for dates are give or not
    published_after = args.get('published_after', '')
    published_before = args.get('published_before', '')
    
    # Parse the dates if they are valid
    try:
        published_after = parse_date(published_after)
        published_before = parse_date(published_before)
    except:
        return jsonify({'error': "Invalid date, date should be passed in ISO format."})

    # Creating a filter dict
    date_filters = {}
    
    if published_after is not None:
        date_filters['$gte'] = published_after
    
    if published_before is not None:
        date_filters['$lte'] = published_before

    query_set = None

    if date_filters:
        query_set = youtube_videos.find({'publishTime': date_filters})
    else:
        query_set = youtube_videos.find()

    # Filter according to the date, descending , and limit to the page size 
    videos = query_set \
            .sort('publishTime', DESCENDING) \
            .skip(page_limit * (page - 1)) \
            .limit(page_limit)

    res = {
        'results': list(json.loads(json_util.dumps(videos)))
    }

    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)