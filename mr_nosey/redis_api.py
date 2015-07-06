import json


class Radio_API(object):

    KEY = "radio|"
    KEY_MATCH = KEY + "*"
    KEY_SEARCH = KEY + "%s"

    def __init__(self, redis):
        self.redis = redis

    def get_radios(self):
        result = map(
            lambda radio: dict(
                json.loads(self.redis.get(radio)).items() +
                {"name": radio.replace(self.KEY, "")}.items()
            ),
            self.redis.scan_iter(match=self.KEY_MATCH)
            )
        return result

    def blank_radios(self):
        """Reasonable to expect this needs to support only
        removing our keys in the future - extremely bad
        citizenship
        """
        self.redis.flushdb()

    def merge_radio(self, radio):
        key = self._key_for_radio(radio)
        del radio["name"]
        self.redis.set(key, json.dumps(radio))

    def get_radio(self, key):
        return self.redis.get(key)

    @staticmethod
    def _key_for_radio(radio):
        assert radio['name'] is not None
        return Radio_API.KEY_SEARCH % (radio["name"])

