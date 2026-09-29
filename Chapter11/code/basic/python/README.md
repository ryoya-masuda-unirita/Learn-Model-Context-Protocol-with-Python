# サンプルの実行

このサンプルは、有効な Authorization ヘッダーがあるかをチェックする middleware 付きの MCP サーバーを起動します。

## 環境のセットアップ

[uv](https://docs.astral.sh/uv/) で依存関係をインストールします（初回のみ）。リポジトリ内のどのディレクトリで実行しても、リポジトリ直下の `.venv` にインストールされます：

```bash
uv sync
```

以降のコマンドは `uv run` を付けて実行します。仮想環境を有効化する必要はありません。

## サーバーの起動

```bash
uv run python server.py
```

別のターミナルでクライアントを起動します：

```bash
uv run python client.py
```

次のような結果になります：

```text
2025-09-30 13:25:54 - mcp_client - INFO - tool の結果: meta=None content=[TextContent(type='text', text='{\n  "current_time": "2025-09-30T13:25:54.311900",\n  "timezone": "UTC",\n  "timestamp": 1759238754.3119,\n  "formatted": "2025-09-30 13:25:54"\n}', annotations=None, meta=None)] structuredContent={'current_time': '2025-09-30T13:25:54.311900', 'timezone': 'UTC', 'timestamp': 1759238754.3119, 'formatted': '2025-09-30 13:25:54'} isError=False
```

これは、送った認証情報が受け入れられたことを意味します。

`client.py` の認証情報を "secret-token2" に変えてみてください。応答の一部として次のテキストが表示されます：

```text
2025-09-30 13:27:44 - httpx - INFO - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 403 Forbidden"
```

これは、認証情報は送られた（認証は行われた）が、その認証情報が無効だったことを意味します。
