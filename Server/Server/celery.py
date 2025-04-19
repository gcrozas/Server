# Sever/celery.py

# Librerias
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Server.settings')

app = Celery('Server') #Nombre del proyecto

app.conf.beat_schedule = {
    'i2creader_60s': {
        'task': 'iot.tasks.i2creader', #Leemos los dispositivos iot por i2c
        # La tarea se ejecuta cada 1 minuto
        'schedule': crontab(minute='*/1')
    },
    'average_data_60m': {
        'task': 'iot.tasks.average_data',
        # La tarea se ejecuta cada 1 hora, en el minuto 1
        'schedule': crontab(minute=1, hour='*/1')
    },
    'turn_on_AC': {
        'task': 'iot.tasks.turn_on_AC',
        # La tarea se ejecuta a las 6:50 am, de Lunes a Viernes
        'schedule': crontab(minute=50, hour=6, day_of_week='mon,tue,wed,thu,fri')
    }
}

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace = 'CELERY' means all celery-related configuration keys
# should have a 'CELERY_' prefix.
app.config_from_object('django.conf:settings',namespace='CELERY')

# Load task modules from all registered Django apps
app.autodiscover_tasks()

"""@app.task(bind=True)
def debug_task(self):
    print(f'Request:  {self.request!r}')"""

"""@app.task
def test(arg):
    print(arg)"""