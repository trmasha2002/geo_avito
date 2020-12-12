import telnetlib
from cacheout import Cache
import re
from fastapi import FastAPI, Request

class Redis(object):
    def __init__(self):
        self._data = Cache()

    def keys(self, pattern):
        result = []
        for key in self._data.keys():
            if re.search(pattern, key) != None:
                result.append(key)
        return result

    def set(self, key, value, ttl=0):
        if ttl != 0:
            self._data.set(key, value, ttl)
        else:
            self._data.set(key, value)
        return 1

    def hset(self, hash, key, value, ttl=0):
        if ttl != 0:
            self._data.set(hash, key, ttl)
            self._data.set(key, value, ttl)
        else:
            self._data.set(hash, key)
            self._data.set(key, value)
        return 1

    def get(self, key):
        return self._data.get(key)

    def hget(self, hash, key):
        find_key = self._data.get(hash)
        if find_key != key:
            return 0
        return self._data.get(find_key)

    def delete(self, key):
        if key in self._data.keys():
            self._data.delete(key)
            return 1
        else:
            return 0



