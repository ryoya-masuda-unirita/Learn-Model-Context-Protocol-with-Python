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
Starting client...
ID:  None
ID:  3b4a5d8fe27947b094d7792acaca1349
Session initialized, ready to call tools.
Received message: root=LoggingMessageNotification(method='notifications/message', params=LoggingMessageNotificationParams(meta=None, level='info', logger=None, data='Processing file 1/3:'), jsonrpc='2.0')
NOTIFICATION: root=LoggingMessageNotification(method='notifications/message', params=LoggingMessageNotificationParams(meta=None, level='info', logger=None, data='Processing file 1/3:'), jsonrpc='2.0')
Received message: root=LoggingMessageNotification(method='notifications/message', params=LoggingMessageNotificationParams(meta=None, level='info', logger=None, data='Processing file 2/3:'), jsonrpc='2.0')
NOTIFICATION: root=LoggingMessageNotification(method='notifications/message', params=LoggingMessageNotificationParams(meta=None, level='info', logger=None, data='Processing file 2/3:'), jsonrpc='2.0')
Received message: root=LoggingMessageNotification(method='notifications/message', params=LoggingMessageNotificationParams(meta=None, level='info', logger=None, data='Processing file 3/3:'), jsonrpc='2.0')
NOTIFICATION: root=LoggingMessageNotification(method='notifications/message', params=LoggingMessageNotificationParams(meta=None, level='info', logger=None, data='Processing file 3/3:'), jsonrpc='2.0')
Tool result: meta=None content=[TextContent(type='text', text="Here's the file content: hello", annotations=None)] isError=False
```

この出力には、すべての通知と tool 呼び出しの結果が表示されています。
