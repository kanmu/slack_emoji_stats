# ========== get_emoji_stats_per_channel_list.py
import json
import os
import sys
from datetime import datetime

from slack_sdk.http_retry import all_builtin_retry_handlers
from slack_sdk.web import WebClient

SLACK_API_TOKEN = os.environ["SLACK_API_TOKEN"]

client = WebClient(token=SLACK_API_TOKEN, retry_handlers=all_builtin_retry_handlers())


# ファイルの存在確認をする関数
def file_exists(file_path):
    try:
        with open(file_path):
            return True
    except FileNotFoundError:
        return False


# メッセージを全件取得する関数
def get_all_messages(channel_id):
    all_messages = []
    cursor = None

    while True:
        response = client.conversations_history(
            channel=channel_id,
            cursor=cursor,
            oldest=datetime(2023, 1, 1).timestamp(),  # 2023年1月1日以降のメッセージを取得
        )

        if response["ok"]:
            messages = response["messages"]

            # threadのparentの場合はthreadのメッセージも取得
            # cf. https://api.slack.com/messaging/retrieving#threading

            for message in messages:
                if message.get("thread_ts"):
                    if message.get("ts") == message.get("thread_ts"):
                        print("Fetching replies...")
                        response_replies = client.conversations_replies(
                                channel=channel_id,
                                ts=message.get("ts"),
                        )

                        if response_replies["ok"]:
                            all_messages.extend(response_replies["messages"])
                else:
                    all_messages.append(message)

            if response["has_more"]:
                print("Fetching more messages...")
                cursor = response["response_metadata"]["next_cursor"]
            else:
                break
        else:
            print("Error fetching history:", response["error"])

            break

    return all_messages


# =========== main
num = sys.argv[1]
input_dir = "tmp_dir"
output_dir = "result_dir"

if not num:
    print("num is required")
    sys.exit(1)

channel_list = []
with open(f"{input_dir}/channel_list_{num}.json", "r") as f:
    channel_list = json.load(f)


total_emoji_counts = {}
emoji_counts_per_user = {}


# チャンネル数に合わせて limitを変更
channel_json_list = []


for channel in channel_list:
    channel_id = channel["id"]
    channel_name = channel["name"]

    json_file_path = f"{output_dir}/{channel_id}_{channel_name}.json"
    channel_json_list.append(json_file_path)

    if file_exists(json_file_path):
        continue

    # 各チャンネルのメッセージを全件取得

    print("channel loop ===================", channel_id)
    try:
        messages = get_all_messages(channel_id)

        for message in messages:
            user_id = message.get("user")

            if not (user_id in emoji_counts_per_user):  # キーがない場合は空の辞書で初期化
                emoji_counts_per_user[user_id] = {}

            emojis = [emoji for emoji in message.get("reactions", [])]

            for emoji in emojis:
                emoji_name = emoji["name"]

                if not (emoji_name in total_emoji_counts):  # キーがない場合は0で初期化
                    total_emoji_counts[emoji_name] = 0
                total_emoji_counts[emoji_name] += emoji["count"]

                if not (emoji_name in emoji_counts_per_user[user_id]):
                    emoji_counts_per_user[user_id][emoji_name] = 0
                emoji_counts_per_user[user_id][emoji_name] += emoji["count"]

        # 結果をファイルに保存
        with open(json_file_path, "w") as f:
            json.dump(emoji_counts_per_user, f, indent=2)

    except Exception as e:
        print("An error occurred:", channel_id, e)

    finally:
        emoji_counts_per_user = {}
