import requests
from tasks.utils.mongo_utils import get_db, get_configs, get_api_keys
from datetime import datetime, timedelta

YOUTUBE_API_URL = 'https://youtube.googleapis.com/youtube/v3/search'
SUBJECT = 'lofi'

def get_the_start_time():
    db = get_db()
    config = get_configs()
    start_from_date = config['last_run']
    current_time = datetime.utcnow()

    if start_from_date == '':
        start_from_date = current_time - timedelta(seconds=1000000)
    
    config['last_run'] = current_time
    db.configs.update_one({'_id': config['_id']}, {'$set': config}, upsert=False)

    start_from_date_str = start_from_date.isoformat('T') + 'Z'
    return start_from_date_str

def fetch_page(published_after, page=''):
    api_keys = get_api_keys()

    if len(api_keys) == 0:
        raise Exception('No youtube api keys found, please add youtube api keys in the configs collection.')

    for api_key in api_keys:
        res = requests.get(YOUTUBE_API_URL, params={
            'part': 'id,snippet',
            'type': 'video',
            'order': 'date',
            'maxResults': 50,
            'q': SUBJECT,
            'key': api_key,
            'publishedAfter': published_after,
            'pageToken': page
        })

        # Try another key
        if res.status_code == 403:
            continue
        # If it's not a key related problem, then raise an exception
        elif res.status_code != 200:
            raise Exception('something went wrong, response - ', res.json())
        else:
            body = res.json()
            videos = body.get('items', [])
            next_page = body.get('nextPageToken', '')
            return videos, next_page

    raise Exception('All of the keys have expired their daily quota !.')

def extract_youtube_data():
    published_after = get_the_start_time()

    page = ''
    total_videos = []

    while True:
        videos, next_page = fetch_page(published_after, page)
        print("fetched ", len(videos))

        total_videos += videos

        if next_page == '':
            return total_videos
        else:
            page = next_page