from flask import Flask, request, jsonify
import json
from app.config import Config
from app.slack_api.slack_client import SlackClient


app = Flask(__name__)
config = Config()
token = config.get("slack", "bot_token")
slack = SlackClient(token)


@app.route("/slack/interact", methods=["POST"])
def slack_events():
    payload = json.loads(request.form.get("payload"))
    action_id = payload["actions"][0]["action_id"]
    trigger_id = payload["trigger_id"]

    return "", 200

 # use NGROK with localhots:3000
if __name__ == "__main__":
    app.run(port=3000)
