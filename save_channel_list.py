import json
import os

from slack_sdk.http_retry import all_builtin_retry_handlers
from slack_sdk.web import WebClient

SLACK_API_TOKEN = os.environ["SLACK_API_TOKEN"]

client = WebClient(token=SLACK_API_TOKEN, retry_handlers=all_builtin_retry_handlers())

# チャンネル数に合わせて limitを変更
channel_list = client.conversations_list(limit=1000)["channels"]
channel_list_len = len(channel_list)

output_dir = "tmp_dir"

for i in range(10):
    one_of_ten = channel_list_len / 10
    tmp_list = []

    if i == 10:
        tmp_list = channel_list[int(one_of_ten * i):]
    else:
        tmp_list = channel_list[int(one_of_ten * i):int(one_of_ten * (i + 1))]

    with open(f"{output_dir}/channel_list_{i}.json", "w") as f:
        json.dump(tmp_list, f, indent=2)
