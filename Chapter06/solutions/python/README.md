# このサンプルの実行

## 環境のセットアップ

[uv](https://docs.astral.sh/uv/) で依存関係をインストールします（初回のみ）。リポジトリ内のどのディレクトリで実行しても、リポジトリ直下の `.venv` にインストールされます：

```bash
uv sync
```

以降のコマンドは `uv run` を付けて実行します。仮想環境を有効化する必要はありません。

## サーバーを試す

サーバーを起動します：

```
cd e-commerce
uv run python server.py
```

別のターミナルで次を実行します。

注文する

```
npx @modelcontextprotocol/inspector --cli http://localhost:8000/sse --method tools/call --tool-name place_order --tool-arg customer_id=1 --tool-arg quantity=1 --tool-arg total_price=100
```

注文を取得する（全件）

```sh
npx @modelcontextprotocol/inspector --cli http://localhost:8000/sse --method tools/call --tool-name get_orders --tool-arg customer_id=0
```
