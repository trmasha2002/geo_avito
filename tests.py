import unittest
from main import Server
class TestServerFunction(unittest.TestCase):
    def test_set_in_redis(self):
        server = Server()
        result = server.set("key", "value")
        assert result == 1
    def test_get_in_redis(self):
        server = Server()
        server.set("key", "value")
        result = server.get("key")
        assert result == "value"
    def test_delete_in_redis(self):
        server = Server()
        server.set("key", "value")
        result = server.delete("key")
        assert result == 1
    def test_keys_in_redis(self):
        server = Server()
        server.set("key", "value")
        result = server.keys("k?y")
        assert result == ["key"]
if __name__ == '__main__':
    unittest.main()
