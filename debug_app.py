from flask import Flask, request, jsonify
import json
from app.config import Config
from app.slack_api.slack_client import SlackClient
from app.slack_api import slack_blocks


app = Flask(__name__)
user_selections = {}
config = Config()
token = config.get("slack", "bot_token")
channel = config.get("slack", "debug_user")
slack = SlackClient(token)


# Конечная точка для обработки событий Slack
@app.route("/slack/interact", methods=["POST"])
def slack_events(selected_project=None, selected_task=None):
    payload = json.loads(request.form.get("payload"))
    actions = payload["actions"]
    action_id = actions[0]["action_id"]
    trigger_id = payload["trigger_id"]
    if action_id == "open_modal_button":
        # Вызов метода для открытия модального окна
        response = slack.open_modal(trigger_id)
    elif action_id in ["select_project", "select_epic_task", "time_select_action"]:
        message = payload["message"]
        # Отправка запроса для обновления сообщения
        response = slack.update_message(
            payload["channel"]["id"],
            message["ts"],
            text=message["text"],
            blocks=slack_blocks.update_selection(message["blocks"], actions),
        )
    elif action_id == "refresh_button":
        message = payload["message"]
        response = slack.update_message(
            payload["channel"]["id"],
            message["ts"],
            text=message["text"],
            blocks=slack_blocks.handle_refresh(message["blocks"]),
        )
    elif action_id == "submit_button":
        # response = slack.open_submit_modal(trigger_id, message["blocks"])
        message = payload["message"]
        response = slack.update_message(
            payload["channel"]["id"],
            message["ts"],
            text=message["text"],
            blocks=slack_blocks.submit_blocks(
                blocks=message["blocks"], date=message["text"]
            ),
        )
    elif action_id == "edit_button":
        message = payload["message"]
        response = slack.update_message(
            payload["channel"]["id"],
            message["ts"],
            text=message["text"],
            blocks=slack_blocks.initial_combined_block(
                slack_blocks.project_data, date=message["text"]
            ),
        )

    # Проверка ответа Slack API для отладки
    if response is not None:
        if isinstance(response, dict) and response.get("success"):
            print("Сообщение успешно обновлено.")
        else:
            print("Ошибка при обновлении:", response)
    else:
        print("nothing to do")

    return "", 200


# todo - add update button with original product data

if __name__ == "__main__":
    app.run(port=3000)
