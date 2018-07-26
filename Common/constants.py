from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CHAT_CONSUMER_PREFIX_GROUP_NAME = 'chat_%s'
USER_STRING = 'USER-PRIVATE-KEY'
ROOM_STRING = 'ROOM-PRIVATE-KEY'
USER_CONTACT_HAVE_ROOM = 'UserHaveRoomWithContact'
USER_EXIST_IN_ROOM = 'UserExistInTheRoom'
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
