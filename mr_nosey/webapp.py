from flask import Flask, jsonify
app = Flask(__name__)


@app.route("/")
def hello():
    data = {"data": "something"}
    return jsonify(data)

if __name__ == "__main__":
    app.run()
