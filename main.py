from cacheout import Cache
import re
class Server(object):
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
    def get(self, key):
        return self._data.get(key)

    def delete(self, key):
        if key in self._data.keys():
            self._data.delete(key)
s = Server()
s.set("firstname", "Maria")
s.set("surname", "Tryapitsyna")
print(s.keys("n?me"))
print(s.get("firstname"))


