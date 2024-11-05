from flask import Flask, jsonify
from app.config import Config


def create_app(debug=False):
    app = Flask(__name__)
    app.config["DEBUG"] = debug
    config = Config(debug=app.config["DEBUG"])

    @app.route("/")
    def index():
        app_name = "Flask app template"
        return jsonify(
            {
                "App": app_name,
            }
        )

    return app
