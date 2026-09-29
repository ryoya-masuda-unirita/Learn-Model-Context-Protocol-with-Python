# サンプルの実行

## セットアップ

```sh
python -m venv venv
source venv/bin/activate
pip install "mcp[cli]"
```

## サーバーの実行

```sh
python server.py
```

## クライアントの実行

```sh
npx @modelcontextprotocol/inspector server.py
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
