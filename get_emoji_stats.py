import csv
import json
import os
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
            oldest=datetime(2023, 1, 1).timestamp,  # 2023年1月1日以降のメッセージを取得
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
                            messages.extend(response_replies["messages"])
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


total_emoji_counts = {}
emoji_counts_per_user = {}


# チャンネル数に合わせて limitを変更
channel_list = client.conversations_list(limit=500)["channels"]
channel_json_list = []


for channel in channel_list:
    channel_id = channel["id"]
    channel_name = channel["name"]

    json_file_path = f"result_dir/{channel_id}_{channel_name}.json"
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


emoji_counts_per_user = {}

# チャンネルごとの結果をロード

for json_file_path in channel_json_list:
    with open(json_file_path) as f:
        emoji_counts_per_user_one_channel = json.load(f)

    for user_id, emoji_dict in emoji_counts_per_user_one_channel.items():
        if not (user_id in emoji_counts_per_user):
            emoji_counts_per_user[user_id] = {}

        for emoji_name, count in emoji_dict.items():
            if not (emoji_name in emoji_counts_per_user[user_id]):
                emoji_counts_per_user[user_id][emoji_name] = 0
            emoji_counts_per_user[user_id][emoji_name] += count

print("csv start ===================")

with open('result.csv', 'w', newline='') as csvfile:
    fieldnames = ["user_id", "user_name", *total_emoji_counts.keys()]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')

    writer.writeheader()

    print(emoji_counts_per_user)

    for user_id, emoji_counts in emoji_counts_per_user.items():
        row = {emoji_name: emoji_counts.get(emoji_name, "") for emoji_name in total_emoji_counts.keys()}
        row["user_id"] = user_id

        try:
            row["user_name"] = client.users_info(user=user_id)["user"]["name"]
        except Exception as e:
            print("An error occurred:", user_id, e)
            row["user_name"] = ""

        writer.writerow(row)

# for debug
with open('result.txt', 'w') as f:
    print(emoji_counts_per_user, file=f)
