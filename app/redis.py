from cacheout import Cache
import re


class Redis(object):
    def __init__(self):
        self._data = Cache()
        self._tokens = Cache()

    def check_token(self, token):
        return token in self._tokens.keys()

    def set_token(self, key, value):
        self._tokens.set(key, value)

    def keys(self, pattern):
        result = []
        for key in self._data.keys():
            if re.search(pattern, key) is not None:
                result.append(key)
        return result

    def set(self, key, value, ttl=None):
        self._data.set(key, value, ttl)
        return 1

    def hset(self, hash, key, value, ttl=None):
        self._data.set(hash, key, ttl)
        self._data.set(key, value, ttl)
        return 1

    def lset(self, name_list, index, value, ttl=None):
        if name_list not in self._data.keys():
            array_of_data = [0 for i in range(index + 1)]
            array_of_data[index] = value
        else:
            array_of_data = self.get(name_list)
            if len(array_of_data) <= index:
                array_of_data += [0 for i in range(index + 1 - len(array_of_data))]
                array_of_data[index] = value
            else:
                array_of_data[index] = value
        self._data.set(name_list, array_of_data, ttl)
        return 1

    def get(self, key):
        return self._data.get(key)

    def hget(self, hash, key):
        find_key = self._data.get(hash)
        if find_key != key:
            return None
        return self._data.get(find_key)

    def lget(self, name_of_list, index):
        array_of_data = self._data.get(name_of_list)
        if array_of_data is None:
            return None
        print(array_of_data)
        if index < len(array_of_data):
            return array_of_data[index]
        else:
            return None

    def delete(self, key):
        if key in self._data.keys():
            self._data.delete(key)
            return 1
        else:
            return None
