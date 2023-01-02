from celery import Celery
from tasks.utils.youtube_utils import extract_youtube_data

app = Celery('tasks', broker='redis://redis:6379')

# Testing celery beat scheduler
app.conf.beat_schedule = {
    'youtube-task': {
        'task': 'youtube_etl',
        'schedule': 3
    }
}

@app.task(name='youtube_etl')
def youtube_etl():
    videos = extract_youtube_data()
    print(videos)