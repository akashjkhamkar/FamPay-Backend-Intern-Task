from celery import Celery

app = Celery('tasks', broker='redis://redis:6379')

# Testing celery beat scheduler
app.conf.beat_schedule = {
    'testing-scheduler': {
        'task': 'hello_world',
        'schedule': 3
    }
}

@app.task(name='hello_world')
def hello_world():
    print("Hello world")