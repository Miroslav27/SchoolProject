from django.urls import path , include
from journal.consumers import ChatConsumer

from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/auction/(?P<uri>[^/]+)', consumers.ChatConsumer.as_asgi()),
]