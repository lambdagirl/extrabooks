from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'extrabooks_app.settings')
app = Celery('extrabooks_app')

app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()

#app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
            #    CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
