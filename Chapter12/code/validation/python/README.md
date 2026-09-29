# サンプルの実行

## 環境のセットアップ

[uv](https://docs.astral.sh/uv/) で依存関係をインストールします（初回のみ）。リポジトリ内のどのディレクトリで実行しても、リポジトリ直下の `.venv` にインストールされます：

```bash
uv sync
```

以降のコマンドは `uv run` を付けて実行します。仮想環境を有効化する必要はありません。

## サーバーの実行

```sh
uv run python server.py
```

## クライアントの実行

```sh
npx @modelcontextprotocol/inspector uv run python server.py
```

サーバーに接続し、tool `create_user` を実行します。

2種類の payload を試して、検証結果の違いを確認してください。

1. 成功する場合（必須フィールドをすべて指定）：

   ```json
   {
     "id": 0,
     "name": "chris",
     "email": "chris@example.com"
   }
   ```

2. 検証エラーになる場合（email を省略しているので、検証が働いていることが分かります）：

   ```json
   {
     "id": 0,
     "name": "chris"
   }
   ```
