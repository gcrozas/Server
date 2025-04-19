# This will make sure the app is always imported when
# Django starts so that shared_task will user this app.
from Server.celery import app as celery_app

__all__= ['celery_app']