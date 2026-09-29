# resumability（再開可能性）を curl で試す

resumability に対応したサーバー（[../resumability/server.py](../resumability/server.py)）に curl でリクエストを送り、途中で切断されたストリームを Last-Event-ID を使って再開する流れを確認します。

## サーバーの起動

```bash
cd ../resumability
uv run python server.py
```

ポート 3000 の `/mcp/` で待ち受けます（`/mcp` に送ると `/mcp/` にリダイレクトされるので、URL の末尾に `/` を付けます）。

## クライアント

### 接続

`-i` を付けて、応答ヘッダーも表示します：

```bash
curl -i -X POST "http://127.0.0.1:3000/mcp/" -H "Accept: text/event-stream, application/json" -H "Content-Type: application/json" -d '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": { "protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": { "name": "ExampleClient", "version": "1.0.0" } }
}'
```

応答ヘッダーの `mcp-session-id` がセッション ID です。以降のリクエストでは、`<セッション ID>` をこの値に置き換えます。

### 初期化

```bash
curl -X POST "http://127.0.0.1:3000/mcp/" -H "Accept: text/event-stream, application/json" -H "Content-Type: application/json" -H "mcp-session-id: <セッション ID>" -d '{
    "jsonrpc": "2.0",
    "method": "notifications/initialized"
}'
```

### tool の呼び出し

```bash
curl -N -X POST "http://127.0.0.1:3000/mcp/" -H "Accept: text/event-stream, application/json" -H "Content-Type: application/json" -H "mcp-session-id: <セッション ID>" -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "process-files",
      "arguments": {}
    }
}'
```

ファイルごとの進捗の通知と最終結果が、SSE のイベントとして返ってきます。各イベントには `id:` でイベント ID が付いています：

```text
id: f518368b-2154-4000-9eb8-9753701dcf83
event: message
data: {"method":"notifications/message","params":{"level":"info","logger":"notification_stream","data":"[1/3] 'file1.txt' からのイベント - 切断された場合は Last-Event-ID を使って再開できます"},"jsonrpc":"2.0"}

id: eb791416-6037-45ea-b8e4-256a5bfba12b
event: message
data: {"method":"notifications/message","params":{"level":"info","logger":"notification_stream","data":"[2/3] 'file2.txt' からのイベント - 切断された場合は Last-Event-ID を使って再開できます"},"jsonrpc":"2.0"}
...
```

### Last-Event-ID を使った再開

最初のイベントまで受け取ったところで切断された、という想定で、そのイベント ID を `last-event-id` ヘッダーに付けて GET します：

```bash
curl -N "http://127.0.0.1:3000/mcp/" -H "Accept: text/event-stream, application/json" -H "mcp-session-id: <セッション ID>" -H "last-event-id: <最初のイベント ID>"
```

サーバーはイベントストアに保存しているイベントのうち、指定した ID より後のもの（2件目以降の通知と最終結果）を再送します。
