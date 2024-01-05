# slack emoji stats

slackのemoji集計のために使うスクリプト。
現状は特定期間の間に各ユーザーが獲得したemojiの集計に使えるのみです。
例えば、特定期間で特定emojiのランキングを出す、という用途では使えません。スクリプト追加してくれると嬉しいです。

## 利用方法

### get_emoji_stats.pyスクリプト
```
pip3 install -r requirements.txt
SLACK_API_TOKEN=<YOUR_PERSONAL_TOKEN> python3 get_emoji_stats.py
```
result.csv, result.txtというファイルが出力されます。
result.txtはデバッグ用です。集計用途にはresult.csvのみ利用すれば良いでしょう。

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
