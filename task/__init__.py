import os

from celery import Celery

from task import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiper.settings')

celery_app = Celery('swiper_task')
celery_app.config_from_object(config)
celery_app.autodiscover_tasks()
