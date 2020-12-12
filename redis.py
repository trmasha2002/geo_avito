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
    def lset(self, name_list, index, value, ttl=0):
        if name_list not in self._data.keys():
            array_of_data = [0 for i in range(index + 1)]
            array_of_data[index] = value
        else:
            array_of_data = self.get(name_list)
            if (len(array_of_data) <= index):
                array_of_data += [0 for i in range(index + 1 - len(array_of_data))]
                array_of_data[index] = value
            else:
                array_of_data[index] = value
        if (ttl == 0):
            self._data.set(name_list, array_of_data)
        else:
            self._data.set(name_list, array_of_data, ttl)
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




