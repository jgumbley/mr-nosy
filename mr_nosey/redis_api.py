import json


class Radio_API(object):

    KEY = "radio|"

    def __init__(self, redis):
        self.redis = redis

    def get_radios(self):
        result = map(
            lambda key: json.loads(self.redis.get(key)),
            self.redis.scan_iter(match="radios|*")
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
        return "radios|%s" % (radio["name"])

