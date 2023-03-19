# celery.py

from celery import Celery

app = Celery('fbs')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()