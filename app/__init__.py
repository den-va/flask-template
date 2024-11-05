from flask import Flask, jsonify
from app.config import Config


def create_app(debug=False):
    app = Flask(__name__)
    app.config["DEBUG"] = debug
    config = Config(debug=app.config["DEBUG"])

    @app.route("/")
    def index():
        app_name = "Time police web app"
        return jsonify(
            {
                "App": app_name,
            }
        )

    return app


if __name__ == "__main__":
    app = create_app(debug=True)
    app.run(host="0.0.0.0", port=6548)
