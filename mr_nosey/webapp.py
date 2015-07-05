import json
from flask import Flask, jsonify, request
from flask_redis import Redis
import uuid

app = Flask(__name__,
            static_url_path='',
            static_folder='frontend'
            )
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))
redis = Redis(app)
app.config['REDIS_HOST'] = 'localhost'
app.config['REDIS_PORT'] = 6379


@app.route("/api")
def hello():
    req_id = str(uuid.uuid1())
    data = {"req_id": req_id,
            "name": "steve",
            "children": [
                {"name": "00:1C:B3:09:85:15",
                 "type": "sta", "ap": "00:1C:B3:09:85:16"},
                {"name": "00:1C:B3:09:85:16",
                 "type": "ap"},
                {"name": "00:1C:B3:09:85:17",
                 "type": "sta", "ap": "00:1C:B3:09:85:16"},
                {"name": str(uuid.uuid1()),
                 "type": "sta", "ap": "00:1C:B3:09:85:16"}
            ]
            }
    return jsonify({"data": data})


def get_radios():
    radios = json.loads(redis.get("radios"))
    if radios is None:
        radios = []
    print radios
    return radios


def set_radios(radios):
    print radios
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
    print jsonify(data=radios)
    return jsonify(data=radios)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
