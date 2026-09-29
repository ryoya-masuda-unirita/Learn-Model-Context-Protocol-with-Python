# サンプルの実行

## 環境のセットアップ

[uv](https://docs.astral.sh/uv/) で依存関係をインストールします（初回のみ）。リポジトリ内のどのディレクトリで実行しても、リポジトリ直下の `.venv` にインストールされます：

```bash
uv sync
```

以降のコマンドは `uv run` を付けて実行します。仮想環境を有効化する必要はありません。

## トークンの生成

テスト用の JWT トークンを、簡単なスクリプトで生成します。

```bash
uv run python util.py
```

トークンが `.env` ファイルに書き出されます。クライアントは dotenv で `.env` ファイルからこのトークンを読み込み、サーバーへの認証に使います。

## サーバーの起動

```bash
uv run python server.py
```

## クライアントの起動

別のターミナルで次を実行します：

```bash
uv run python client.py
```

次のような出力になります：

```text
有効なトークンです。処理を続けます...
ユーザーが存在します。処理を続けます...
ユーザーは必要な scope を持っています。処理を続けます...
```

トークンが無効な場合の動きを見たいときは、`util.py` の payload を変えて無効なトークンを生成します。たとえば次のように、scopes をサーバーが期待する "Admin.Write" ではなく "User.Write" に変えます：

```python
payload = {
        "sub": "1234567890",               # サブジェクト（ユーザー ID）
        "name": "User Userson",                # カスタム claim
        "admin": True,                     # カスタム claim
        "iat": datetime.datetime.now(datetime.timezone.utc),# 発行日時
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),  # 有効期限
        "scopes": ["User.Write"]  # scope（権限）用のカスタム claim
    }
```
