import json


class Radio_API(object):

    KEY = "radio|"

    def __init__(self, redis):
        self.redis = redis

    def get_radios(self):
        result = []
        for key in self.redis.scan_iter(match="radios|*"):
            result.append(
                json.loads(self.redis.get(key))
            )
        return result

    def set_radios(self, radios):
        self.redis.set("radios", json.dumps(radios))

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

