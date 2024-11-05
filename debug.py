from app.config import Config
from app.slack_api.slack_client import SlackClient

if __name__ == "__main__":
    config = Config()
    token = config.get("slack", "bot_token")
    channel = config.get("slack", "debug_user")
    # channel = config.get("slack", "debug_channel")
    slack = SlackClient(token)
    result = slack.send_initial_block(channel, "2024-01-01")
    # result = slack.clear_chat("D07TT531YF9")
    # send to user id, chat.update channel id D07TT531YF9
    print(result)
