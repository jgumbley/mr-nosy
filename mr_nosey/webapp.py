from flask import Flask, jsonify
import uuid
app = Flask(__name__,
            static_url_path='',
            static_folder='frontend'
            )
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))


@app.route("/api")
def hello():
    data = {"data": str(uuid.uuid1())}
    return jsonify(data)

if __name__ == "__main__":
    app.run()
