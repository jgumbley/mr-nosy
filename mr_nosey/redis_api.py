import json


class RadioAPI(object):

    KEY = "radio|"
    KEY_MATCH = KEY + "*"
    KEY_SEARCH = KEY + "%s"

    def __init__(self, redis):
        self.redis = redis

    def get_radios(self):
        result = map(
            lambda key: dict(
                self.get_radio(key).items() +
                {"name": key.replace(self.KEY, "")}.items()
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
        current = self.get_radio(key)
        if current:
            radio.update(current)
        self.set_radio(radio)

    def set_radio(self, radio):
        key = self._key_for_radio(radio)
        del radio["name"]
        self.redis.set(key, json.dumps(radio))

    def get_radio(self, key):
        if self.redis.exists(key):
            return json.loads(self.redis.get(key))
        else:
            return None

    @staticmethod
    def _key_for_radio(radio):
        assert radio['name'] is not None
        return RadioAPI.KEY_SEARCH % (radio["name"])
