"""Celery app conf"""
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery("app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'schedule_sync_for_all_addresses': {
        'task': 'tracker.tasks.schedule_sync_for_all_addresses',
        'schedule': crontab(hour=5)
    }
}
