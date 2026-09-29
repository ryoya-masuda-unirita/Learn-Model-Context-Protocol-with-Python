# このサンプルの実行

## 依存関係のインストール

まず、仮想環境を作成します：

```sh
python -m venv venv
source ./venv/bin/activate
```

```sh
pip install "mcp[cli]"
```

## サーバーを試す

サーバーを起動します：

```
cd e-commerce
python server.py
```

別のターミナルで次を実行します。

注文する

```
npx @modelcontextprotocol/inspector --cli http://localhost:8000/sse --method tools/call --tool-name place_order --tool-arg order_id=0 --tool-arg customer_id=1 --tool-arg quantity=1 --tool-arg total_price=100
```

注文を取得する（全件）

```sh
npx @modelcontextprotocol/inspector --cli http://localhost:8000/sse --method tools/call --tool-name get_orders --tool-arg customer_id=0
```
