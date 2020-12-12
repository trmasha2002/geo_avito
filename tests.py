import unittest
from redis import Redis
class TestRedisFunctional(unittest.TestCase):
    def test_set_in_redis(self):
        redis = Redis()
        result = redis.set("key", "value")
        assert result == 1

    def test_get_in_redis(self):
        redis = Redis()
        redis.set("key", "value")
        result = redis.get("key")
        assert result == "value"

    def test_delete_in_redis(self):
        redis = Redis()
        redis.set("key", "value")
        result = redis.delete("key")
        assert result == 1

    def test_keys_in_redis(self):
        redis = Redis()
        redis.set("key", "value")
        result = redis.keys("k?y")
        assert result == ["key"]

    def test_hset_in_redis(self):
        redis = Redis()
        result = redis.hset(1,"key", "value")
        assert result == 1

    def test_hget_in_redis(self):
        redis = Redis()
        redis.hset(1, "key", "value")
        result = redis.hget(1, "key")
        assert result == "value"

if __name__ == '__main__':
    unittest.main()
