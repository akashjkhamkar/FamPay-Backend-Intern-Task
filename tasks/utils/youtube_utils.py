import requests
from tasks.utils.mongo_utils import get_db, get_configs, get_api_keys
from datetime import datetime, timedelta

YOUTUBE_API_URL = 'https://youtube.googleapis.com/youtube/v3/search'
SUBJECT = 'football'

def update_last_run_time(time):
    db = get_db()
    config = get_configs()

    config['last_run'] = time
    db.configs.update_one({'_id': config['_id']}, {'$set': config}, upsert=False)

def get_the_start_time():
    """Return the last job execution date."""
    config = get_configs()
    start_from_date = config['last_run']
    current_time = datetime.utcnow()

    if start_from_date == '':
        start_from_date = current_time - timedelta(days=5)
    
    start_from_date_str = start_from_date.isoformat('T') + 'Z'
    return start_from_date_str, current_time

def fetch_page(published_after, api_keys, page=''):
    """Fetch a single page of the youtube data for the given startdate."""
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
    """Fetch youtube data for the given startdate."""
    api_keys = get_api_keys()
    published_after, current_time = get_the_start_time()

    page = ''
    total_videos = []

    # Keep on fetching all the pages, until there is no next page left
    while True:
        videos, next_page = fetch_page(published_after, api_keys, page)
        print("fetched ", len(videos))

        total_videos += videos

        if next_page == '':
            update_last_run_time(current_time)
            return total_videos
        else:
            page = next_page