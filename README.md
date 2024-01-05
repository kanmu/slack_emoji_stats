# slack emoji stats

slackのemoji集計のために使うスクリプト。
現状は特定期間の間に各ユーザーが獲得したemojiの集計に使えるのみです。
例えば、特定期間で特定emojiのランキングを出す、という用途では使えません。スクリプト追加してくれると嬉しいです。

## 利用方法

### get_slack_data.pyスクリプト
```
pip3 install -r requirements.txt
SLACK_API_TOKEN=<YOUR_PERSONAL_TOKEN> python3 get_slack_data.py
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
