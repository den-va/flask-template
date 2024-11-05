from slack_bolt import App
import time


class SlackClient:
    def __init__(self, token):
        self.slack_app = App(token=token)

    def send_message(self, channel, text):
        try:
            response = self.slack_app.client.chat_postMessage(
                channel=channel, text=text
            )
            if response["ok"]:
                # todo log(response) if debug
                return {
                    "success": True,
                    "message_id": response["ts"],
                    "channel": response["channel"],
                    "message": response["message"],
                }
            else:
                raise Exception(f"Error sending message: {response}")
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update_message(self, channel_id, message_id, text=None, blocks=None):
        try:
            response = self.slack_app.client.chat_update(
                channel=channel_id, ts=message_id, text=text, blocks=blocks
            )
            if response["ok"]:
                return {
                    "success": True,
                    "message_id": response["ts"],
                    "channel": response["channel"],
                    "message": response["message"],
                }
            else:
                raise Exception(f"Error updating message: {response}")
        except Exception as e:
            return {"success": False, "error": str(e)}


    def delete_message(self, channel_id, message_id):
        try:
            self.slack_app.client.chat_delete(channel=channel_id, ts=message_id)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def clear_chat(self, channel_id):
        try:
            has_more = True
            while has_more:
                response = self.slack_app.client.conversations_history(
                    channel=channel_id
                )
                messages = response["messages"]
                has_more = response["has_more"]
                for message in messages:
                    try:
                        print(f"deleting message {message['ts']}")
                        self.delete_message(channel_id, message["ts"])
                        time.sleep(
                            0.2
                        ) 
                    except Exception as e:
                        print(f"Error deleting message: {e.response['error']}")
        except Exception as e:
            print(f"Error fetching messages: {e.response['error']}")

    def test_connection(self):
        try:
            self.slack_app.client.auth_test()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
