from hamcrest import assert_that, equal_to
import unittest
import webapp
import json


class WebappTestCase(unittest.TestCase):
    def setUp(self):
        self.app = webapp.app.test_client()

    def test_add_radio_to_empty(self):
        # given
        radio = {"name": "a mac address"}

        # when
        self.app.post("/api/merge_radio", radio)
        # then
        result = self.app.get("/api/all_radios")
        assert_that(json.loads(result.data), equal_to(radio))
