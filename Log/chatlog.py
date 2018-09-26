import datetime
from django.core.cache import cache
from Common import constants


def ConsumerLog(funcName, boolean = None, between = '', data = '', endString = 'hello'):
    date = ''
    if boolean:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cache.set(funcName+date+between+data, endString, timeout=constants.CACHE_TTL)
    


