import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_hp.settings')

app = Celery('hotel_hp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
