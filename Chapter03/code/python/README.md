# サンプルの実行

## 環境のセットアップ

[uv](https://docs.astral.sh/uv/) で依存関係をインストールします（初回のみ）。リポジトリ内のどのディレクトリで実行しても、リポジトリ直下の `.venv` にインストールされます：

```bash
uv sync
```

以降のコマンドは `uv run` を付けて実行します。仮想環境を有効化する必要はありません。

## コードの実行

```bash
uv run mcp run server.py
```

## Inspector の実行

```bash
uv run mcp dev server.py
```

Web 画面が開くはずです。次のように選択してください：

- transport は "stdio"
- command：**mcp**
- arguments：**run server.py**

その後、"Connect" ボタンを押します。
