# サンプルの実行

## 環境の設定

```sh
python -m venv venv
source ./venv/bin/activate
```

## 依存関係のインストール

```bash
pip install "mcp[cli]" dotenv PyJWT
```

## トークンの生成

テスト用の JWT トークンを、簡単なスクリプトで生成します。

```bash
python util.py
```

トークンが `.env` ファイルに書き出されます。クライアントは dotenv で `.env` ファイルからこのトークンを読み込み、サーバーへの認証に使います。

## サーバーの起動

```bash
python server.py
```

## クライアントの起動

別のターミナルで次を実行します：

```bash
python client.py
```

次のような出力になります：

```text
Valid token, proceeding...
User exists, proceeding...
User has required scope, proceeding...
```

トークンが無効な場合の動きを見たいときは、`util.py` の payload を変えて無効なトークンを生成します。たとえば次のように、scopes をサーバーが期待する "Admin.Write" ではなく "User.Write" に変えます：

```python
payload = {
        "sub": "1234567890",               # Subject (user ID)
        "name": "User Userson",                # Custom claim
        "admin": True,                     # Custom claim
        "iat": datetime.datetime.utcnow(),# Issued at
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Expiry
        "scopes": ["User.Write"]  # Custom claim for scopes/permissions
    }
```
