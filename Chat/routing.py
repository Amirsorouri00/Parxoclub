from django.conf.urls import url

from . import consumer
# Django
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

cache.set('urlpattern', 'hello', timeout=CACHE_TTL)

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<privatekey>[^/]+)/(?P<senderprivatekey>[^/]+)/$', consumer.ChatConsumer),
]