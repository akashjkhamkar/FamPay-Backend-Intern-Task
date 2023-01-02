from celery import Celery
from tasks.utils.youtube_utils import extract_youtube_data
from tasks.utils.mongo_utils import load_into_db

app = Celery('tasks', broker='redis://redis:6379')

# Celery beat configuration for the periodic youtube job
app.conf.beat_schedule = {
    'youtube-task': {
        'task': 'youtube_etl',
        'schedule': 10
    }
}

@app.task(name='youtube_etl')
def youtube_etl():
    """Youtube job that runs periodically to fetch youtube video data."""
    videos = extract_youtube_data()
    load_into_db(videos)