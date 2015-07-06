import json
from flask import Flask, jsonify, request
from flask_redis import Redis

app = Flask(__name__,
            static_url_path='',
            static_folder='frontend'
            )
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))
redis = Redis(app)
app.config['REDIS_HOST'] = 'localhost'
app.config['REDIS_PORT'] = 6379


class Radio_API(object):
    def get_radios(self):
        redis.scan()
        radios = json.loads(redis.get("radios"))
        if radios is None:
            radios = []
        return radios

    def set_radios(self, radios):
        redis.set("radios", json.dumps(radios))

    def blank_radios(self):
        self.set_radios([])

    def merge_radio(self, radio):
        radios = self.get_radios()
        radios.append(radio)
        self.set_radios(radios)

radio_api = Radio_API()


@app.route("/api/blank_radios", methods=['POST'])
def blank_radios():
    radio_api.blank_radios()
    return "hello"


@app.route("/api/merge_radio", methods=['POST'])
def merge_radio():
    radio = request.json
    radio_api.merge_radio(radio)
    return "hello"


@app.route("/api/all_radios", methods=['GET'])
def all_radios():
    radios = radio_api.get_radios()
    return jsonify(data={"radios": radios})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
