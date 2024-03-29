# slack emoji stats

slackのemoji集計のために使うスクリプト。
現状は特定期間の間に各ユーザーが獲得したemojiの集計に使えるのみです。
例えば、特定期間で特定emojiのランキングを出すところまでは実装していません。スクリプト追加してくれると嬉しいです。


## 利用方法

### get_emoji_stats.pyスクリプト
```
pip3 install -r requirements.txt

# channel_listが10分割されて出力される
SLACK_API_TOKEN=<YOUR_PERSONAL_TOKEN> python3 save_channel_list.py

# どのchannel_listを処理するのかを引数(0~9)で渡す. 並列で動かすのはおすすめしない。rate limitにより。
SLACK_API_TOKEN=<YOUR_PERSONAL_TOKEN> python3 get_emoji_stats_per_channel_list.py 0

# user単位で集計する
SLACK_API_TOKEN=<YOUR_PERSONAL_TOKEN> python3 aggregate_csv_stats.py

# 必要なemojiだけに絞り込む
python3 csv_minify.py
```
result.csv, result2.csvというファイルが出力されます。
各scriptで、input_dir/output_dirなどの変数があるので、その値を更新することで、出力先を変更することができます


## 事前準備
- python3をローカルにインストールしてください。
    - 動作確認は python3.11.4 で行いました。
- SLACK_API_TOKENを発行するためにSLACK APPをOrganizationに追加してください。
- `User OAuth Token`を使ってください。「参加していないがPublic」なチャンネルのメッセージを取得するために必要です。`Bot User OAuth Token`ではできません。
- API実行のために以下のPermissionを`User OAuth Token`に付与してください。
    - `channels:history`
    - `groups:history`
    - `im:history`
    - `mpim:history`
    - `reactions:read`
    - `userss:read`
    - `channels:read`
    - `groups:read`
    - `im:read`
    - `mpim:read`


## 参考リンク
- [Web API methods | Slack](https://api.slack.com/methods)
- [slack_sdk API documentation](https://slack.dev/python-slack-sdk/api-docs/slack_sdk/)
- [社内でのSlack絵文字使用頻度を集計してみた！ ｜ 株式会社プロトソリューション](https://www.protosolution.co.jp/approach/fuku-lab/20230914)
- [Bolt for Pythonを使ったSlackアプリでratelimitedエラーに対応するには #Python - Qiita](https://qiita.com/geeorgey/items/eff73ea4c045ef4633d1)
