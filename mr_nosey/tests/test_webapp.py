from hamcrest import assert_that, equal_to
import unittest
import webapp
import json


class WebappTestCase(unittest.TestCase):
    def setUp(self):
        self.app = webapp.app.test_client()

    def app_jsonpost(self, uri, data):
        jsonified = json.dumps(data)
        self.app.post(uri, data=jsonified,
                      content_type='application/json')

    def app_allradios(self):
        result = self.app.get("/api/all_radios")
        return json.loads(result.data)["data"]

    def app_blankradios(self):
        self.app.post("/api/blank_radios")

    def test_empty_radios(self):
        self.app_blankradios()
        # then
        assert_that(self.app_allradios(), equal_to([]))

    def test_add_radio_to_empty(self):
        # given
        self.app_blankradios()
        radio = {u"name": u"a mac address"}
        # when
        self.app_jsonpost("/api/merge_radio", radio)
        # then
        assert_that(self.app_allradios(), equal_to([radio]))

    def test_add_another_radio(self):
        # given
        radio = {u"name": u"a mac address"}
        radio2 = {u"name": u"another mac address"}
        # when
        self.app_jsonpost("/api/merge_radio", radio)
        self.app_jsonpost("/api/merge_radio", radio2)
        # then
        both_radios = [radio, radio2]
        assert_that(self.app_allradios(), equal_to(both_radios))

