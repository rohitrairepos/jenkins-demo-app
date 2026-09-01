import unittest

from app import Handler


class DemoAppTest(unittest.TestCase):
    def test_health_endpoint_is_defined(self):
        self.assertTrue(hasattr(Handler, "do_GET"))


if __name__ == "__main__":
    unittest.main()
