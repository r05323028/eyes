'''Eyes celery app module
'''
from celery import Celery

from eyes.config import CeleryConfig

# load celery
config = CeleryConfig()
app = Celery()
app.config_from_object(config)
app.autodiscover_tasks(config.installed_apps)
