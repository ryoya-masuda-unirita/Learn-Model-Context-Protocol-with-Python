# サンプルの実行

## 環境のセットアップ

[uv](https://docs.astral.sh/uv/) で依存関係をインストールします（初回のみ）。リポジトリ内のどのディレクトリで実行しても、リポジトリ直下の `.venv` にインストールされます：

```bash
uv sync
```

以降のコマンドは `uv run` を付けて実行します。仮想環境を有効化する必要はありません。

## サーバーの実行

```sh
uv run uvicorn server:app
```

## サーバーのテスト

```bash
uv run mcp dev server.py
```

