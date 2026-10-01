# このサンプルの実行

このサンプルには2種類のストリーミングサーバーがあります：

- SSE (Server-Sent Events)
- Streaming HTTP

## 環境のセットアップ

[uv](https://docs.astral.sh/uv/) で依存関係をインストールします（初回のみ）。リポジトリ内のどのディレクトリで実行しても、リポジトリ直下の `.venv` にインストールされます：

```bash
uv sync
```

以降のコマンドは `uv run` を付けて実行します。仮想環境を有効化する必要はありません。

## SSE サンプルの実行

サーバーを起動します：

```bash
uv run python sse.py
```

クライアントが接続すると、サーバーのコンソールに次のように表示されます：

```text
ポート 8000 で SSE サーバーを起動しています...
```

別のターミナルでクライアントを起動します：

```bash
uv run python sse_client.py 
```

クライアントのコンソールには次のような出力が表示されます：

```text
SSE を受信: data: Sun Jun  1 18:48:42 2025
SSE を受信: data: Sun Jun  1 18:48:43 2025
SSE を受信: data: Sun Jun  1 18:48:44 2025
SSE を受信: data: Sun Jun  1 18:48:45 2025
SSE を受信: data: Sun Jun  1 18:48:46 2025
SSE を受信: data: 5 件のメッセージを送信しました。接続を閉じます。
```

## Streaming HTTP サンプルの実行

サーバーを起動します：

```bash
uv run python streaming.py
```

クライアントが接続すると、サーバーのコンソールに次のように表示されます：

```text
ポート 8000 でストリーミングサーバーを起動しています...
```

別のターミナルでクライアントを起動します：

```bash
uv run python streaming_client.py
```
クライアントのコンソールには次のような出力が表示されます：

```text
{"message": "こんにちは、世界！"}
{"message": "こんにちは、世界！"}
{"message": "こんにちは、世界！"}
{"message": "こんにちは、世界！"}
{"message": "こんにちは、世界！"}
5 件のメッセージに達しました。接続を閉じます。
```
