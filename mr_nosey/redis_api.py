import json


class Radio_API(object):

    KEY = "radio|"
    KEY_MATCH = KEY + "*"
    KEY_SEARCH = KEY + "%s"

    def __init__(self, redis):
        self.redis = redis

    def get_radios(self):
        result = map(
            lambda radio: json.loads(self.redis.get(radio)),
            self.redis.scan_iter(match=self.KEY_MATCH)
            )
        return result

    def blank_radios(self):
        self.redis.flushdb()

    def merge_radio(self, radio):
        key = self._key_for_radio(radio)
        self.redis.set(key, json.dumps(radio))

    def get_radio(self, key):
        return self.redis.get(key)

    @staticmethod
    def _key_for_radio(radio):
        assert radio['name'] is not None
        return Radio_API.KEY_SEARCH % (radio["name"])

