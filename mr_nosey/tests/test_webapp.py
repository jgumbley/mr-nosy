from hamcrest import assert_that, equal_to
import unittest
import webapp


class WebappTestCase(unittest.TestCase):
    def setUp(self):
        self.app = webapp.app.test_client()

    def test_hello_world(self):
        result = self.app.get("/api")
        assert_that(result.data, equal_to('{\n  "data": "something"\n}'))
