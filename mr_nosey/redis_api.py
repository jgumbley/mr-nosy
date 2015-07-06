import json


class Radio_API(object):
    def __init__(self, redis):
        self.redis = redis

    def get_radios(self):
        self.redis.scan()
        radios = json.loads(self.redis.get("radios"))
        if radios is None:
            radios = []
        return radios

    def set_radios(self, radios):
        self.redis.set("radios", json.dumps(radios))

    def blank_radios(self):
        self.set_radios([])

    def merge_radio(self, radio):
        radios = self.get_radios()
        radios.append(radio)
        self.set_radios(radios)

