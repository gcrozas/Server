from django.urls import re_path
from .consumers import Lab2Consumer, RecordConsumer

ws_urlpatterns = [
    re_path(r'ws/lab-one/',Lab2Consumer.as_asgi()),
    re_path(r'ws/lab-two/',RecordConsumer.as_asgi()),
]