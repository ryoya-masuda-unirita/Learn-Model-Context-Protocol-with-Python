# サンプルの実行

## クライアント

接続

```bash
curl -X POST "http://127.0.0.1:8000/mcp" -H "Accept: text/event-stream, application/json" -H "Content-Type: application/json" -d '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": { "protocolVersion": "2025-03-26", "capabilities": { "tools": {}, "logging": {} }, "clientInfo": { "name": "ExampleClient", "version": "1.0.0" } }
}'
```

d81eb3a0-eb26-4e79-96a5-64bfd409a3f3

初期化

```bash
curl -X POST "http://127.0.0.1:8000/mcp" -H "Content-Type: application/json" -H "Accept: text/event-stream, application/json" -H "mcp-session-id: d81eb3a0-eb26-4e79-96a5-64bfd409a3f3" -d '{
    "jsonrpc": "2.0",
    "method": "notifications/initialized"
}'

```

tool の呼び出し

```bash
curl -X POST "http://127.0.0.1:8000/mcp" -H "Content-Type: application/json" -H "Accept: text/event-stream, application/json" -H "mcp-session-id: d81eb3a0-eb26-4e79-96a5-64bfd409a3f3" -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "process-files",
      "arguments": { "message": "chris" }
    }
}'
```

もう一度 tool を呼び出します。今度は次の last-event-id を指定します：bc0898d8-c66b-4355-9c0c-9f1de74c1535_1757283309847_ispthgge

```bash
curl "http://127.0.0.1:8000/mcp" -H "Content-Type: application/json" -H "Accept: text/event-stream, application/json" -H "mcp-session-id: d81eb3a0-eb26-4e79-96a5-64bfd409a3f3" -H "last-event-id: bc0898d8-c66b-4355-9c0c-9f1de74c1535_1757283309847_ispthgge"
```