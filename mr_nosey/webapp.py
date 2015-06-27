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
                { "name": "steve"},
                { "name": "banny"},
                { "name": "egg"},
            ]
            }
    return jsonify({"data": data})

if __name__ == "__main__":
    app.run()
