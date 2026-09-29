# このサンプルの実行

## 依存関係のインストール

```sh
pip install "mcp[cli]"
```

## サーバーの起動

まず、仮想環境を作成して有効化します：

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

ターミナルで次のコマンドを実行して、サーバーを起動します：

```bash
python server.py
```

次に、別のターミナルでクライアントを実行します：

```bash
python client.py
```

次のような出力が表示されます：

```text
クライアントを起動しています...
ID:  None
ID:  3b4a5d8fe27947b094d7792acaca1349
セッションを初期化しました。tool を呼び出せます。
メッセージを受信: root=LoggingMessageNotification(method='notifications/message', params=LoggingMessageNotificationParams(meta=None, level='info', logger=None, data='ファイルを処理中 1/3:'), jsonrpc='2.0')
通知: root=LoggingMessageNotification(method='notifications/message', params=LoggingMessageNotificationParams(meta=None, level='info', logger=None, data='ファイルを処理中 1/3:'), jsonrpc='2.0')
メッセージを受信: root=LoggingMessageNotification(method='notifications/message', params=LoggingMessageNotificationParams(meta=None, level='info', logger=None, data='ファイルを処理中 2/3:'), jsonrpc='2.0')
通知: root=LoggingMessageNotification(method='notifications/message', params=LoggingMessageNotificationParams(meta=None, level='info', logger=None, data='ファイルを処理中 2/3:'), jsonrpc='2.0')
メッセージを受信: root=LoggingMessageNotification(method='notifications/message', params=LoggingMessageNotificationParams(meta=None, level='info', logger=None, data='ファイルを処理中 3/3:'), jsonrpc='2.0')
通知: root=LoggingMessageNotification(method='notifications/message', params=LoggingMessageNotificationParams(meta=None, level='info', logger=None, data='ファイルを処理中 3/3:'), jsonrpc='2.0')
tool の結果: meta=None content=[TextContent(type='text', text='ファイルの内容です: こんにちは', annotations=None)] isError=False
```

この出力には、すべての通知と tool 呼び出しの結果が表示されています。
