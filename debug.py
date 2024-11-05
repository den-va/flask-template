from app.config import Config
from app.slack_api.slack_client import SlackClient

if __name__ == "__main__":
    config = Config()
    token = config.get("slack", "bot_token")
    channel = config.get("slack", "debug_user")
    slack = SlackClient(token)
    result = slack.send_message(channel, "2024-01-01")
    print(result)
