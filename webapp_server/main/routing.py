from django.urls import path, re_path , include
from main.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<chat_id>\d+)/$', ChatConsumer.as_asgi()) , 
] 