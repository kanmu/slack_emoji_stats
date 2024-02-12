# ========== aggregate_csv_stats.py
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


# =========== main
channel_list = []
input_dir = "tmp_dir"
output_dir = "result_dir"
aggregate_file = "result.csv"

for i in range(10):
    with open(f"{input_dir}/channel_list_{i}.json", "r") as f:
        channel_list.extend(json.load(f))

emoji_list = []  # emojiの種類取得用
emoji_counts_per_user = {}


channel_json_list = []

for channel in channel_list:
    channel_id = channel["id"]
    channel_name = channel["name"]

    json_file_path = f"{output_dir}/{channel_id}_{channel_name}.json"

    if file_exists(json_file_path):
        channel_json_list.append(json_file_path)


# チャンネルごとの結果をロード

for json_file_path in channel_json_list:
    with open(json_file_path) as f:
        emoji_counts_per_user_one_channel = json.load(f)

    for user_id, emoji_dict in emoji_counts_per_user_one_channel.items():
        if not (user_id in emoji_counts_per_user):
            emoji_counts_per_user[user_id] = {}

        for emoji_name, count in emoji_dict.items():
            emoji_list.append(emoji_name)

            if not (emoji_name in emoji_counts_per_user[user_id]):
                emoji_counts_per_user[user_id][emoji_name] = 0
            emoji_counts_per_user[user_id][emoji_name] += count


emoji_list = list(set(emoji_list))  # 重複削除
emoji_list.sort()

print("csv start ===================")

with open(aggregate_file, 'w', newline='') as csvfile:
    fieldnames = ["user_id", "user_name", *emoji_list]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')

    writer.writeheader()

    # print(emoji_counts_per_user)

    for user_id, emoji_counts in emoji_counts_per_user.items():
        row = {emoji_name: emoji_counts.get(emoji_name, "") for emoji_name in emoji_list}
        row["user_id"] = user_id

        try:
            row["user_name"] = client.users_info(user=user_id)["user"]["name"]
        except Exception as e:
            print("An error occurred:", user_id, e)
            row["user_name"] = ""

        writer.writerow(row)
