# daily_report

日報作成を5分で終わらせるためのCLIツールです。自由形式のメモをMarkdown日報に整形し、Slack Incoming Webhookへ投稿できます。

## インストール

```bash
pip install -e .
```

## 使い方

### 対話的にMarkdownを生成

```bash
daily-report
```

各セクションの入力を求められたら、複数行のテキストを入力し、完了したら `Ctrl-D` (Windows は `Ctrl-Z`) を押してください。生成されたMarkdownが標準出力に表示されます。

### オプション引数

- `--activities`, `--learnings`, `--todos`: ファイルパスまたは直接テキストを渡せます。
- `--date`: 日付を `YYYY-MM-DD` 形式で指定。省略時は今日の日付。
- `--json`: Markdownと分解された各セクションをJSONで出力します。
- `--post`: Slackへ投稿します。Webhook URLは`--webhook-url`または環境変数`SLACK_WEBHOOK_URL`で指定します。

### 例: メモファイルから生成してSlackに投稿

```bash
daily-report \
  --activities activities.txt \
  --learnings learnings.txt \
  --todos todos.txt \
  --post \
  --webhook-url https://hooks.slack.com/services/XXXXX/YYYYY/ZZZZZ
```

## Slack Webhookについて

Slack Appの「Incoming Webhooks」を利用してください。Webhook URLの取り扱いにはご注意ください。CLIから直接指定せず、`SLACK_WEBHOOK_URL` 環境変数に設定することを推奨します。

## テスト

```bash
pytest
```
