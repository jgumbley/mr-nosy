from flask import Flask, jsonify
import uuid

app = Flask(__name__,
            static_url_path='',
            static_folder='frontend'
            )
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))


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


@app.route("/api/all_radios")
def all_radios():
    return jsonify({"name": "a mac address"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
