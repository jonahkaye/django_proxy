import os

from celery import Celery
import logging
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genhealth.settings')

app = Celery('genhealth')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.result_backend = settings.CELERY_BROKER_URL
logging.warning(f"[DEBUG]: REDIS CONF {app.conf.broker_url}")

