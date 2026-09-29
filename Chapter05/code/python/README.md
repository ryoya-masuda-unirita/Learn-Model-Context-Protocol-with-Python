# このサンプルの実行

このサンプルには2種類のストリーミングサーバーがあります：

- SSE (Server-Sent Events)
- Streaming HTTP

## 仮想環境の作成

```bash
python -m venv venv
```

## 仮想環境の有効化

**Windows の場合**

```bash
.\venv\Scripts\activate
```

**macOS / Linux の場合**


```bash
source venv/bin/activate
```

## 依存関係のインストール

```bash
pip install Flask requests
```

## SSE サンプルの実行

サーバーを起動します：

```bash
python sse.py
```

クライアントが接続すると、サーバーのコンソールに次のように表示されます：

```text
HTTP streaming server running on port 8000
Starting SSE server on port 8000...
```

別のターミナルでクライアントを起動します：

```bash
python sse_client.py 
```

クライアントのコンソールには次のような出力が表示されます：

```text
Received SSE: data: Sun Jun  1 18:48:42 2025
Received SSE: data: Sun Jun  1 18:48:43 2025
Received SSE: data: Sun Jun  1 18:48:44 2025
Received SSE: data: Sun Jun  1 18:48:45 2025
Received SSE: data: Sun Jun  1 18:48:46 2025
Received SSE: data: 5 messages sent, closing connection.
```

## Streaming HTTP サンプルの実行

サーバーを起動します：

```bash
python streaming_http_server.py
```

クライアントが接続すると、サーバーのコンソールに次のように表示されます：

```text
Streaming HTTP server running on port 8000
Streaming HTTP connection established
```

別のターミナルでクライアントを起動します：

```bash
python streaming_http_client.py
```
クライアントのコンソールには次のような出力が表示されます：

```text
2025-06-01T15:10:43.193Z
2025-06-01T15:10:44.197Z
2025-06-01T15:10:45.205Z
2025-06-01T15:10:46.209Z
2025-06-01T15:10:47.211Z
```
