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


def get_radios():
    radios = json.loads(redis.get("radios"))
    if radios is None:
        radios = []
    return radios


def set_radios(radios):
    redis.set("radios", json.dumps(radios))


@app.route("/api/blank_radios", methods=['POST'])
def blank_radios():
    set_radios([])
    return "hello"


@app.route("/api/merge_radio", methods=['POST'])
def merge_radio():
    radios = get_radios()
    radios.append(request.json)
    set_radios(radios)
    return "hello"


@app.route("/api/all_radios", methods=['GET'])
def all_radios():
    radios = get_radios()
    return jsonify(data={"radios": radios})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
