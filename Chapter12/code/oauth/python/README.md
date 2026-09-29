# OAuth サンプルの実行


## -0- 環境のセットアップ

[uv](https://docs.astral.sh/uv/) で依存関係をインストールします（初回のみ）。リポジトリ内のどのディレクトリで実行しても、リポジトリ直下の `.venv` にインストールされます：

```bash
uv sync
```

以降のコマンドは `uv run` を付けて実行します。仮想環境を有効化する必要はありません。

## -1- 認可サーバーの起動

```sh
uv run python auth-server.py
```

ポート 5050 で起動します。

> macOS ではポート 5000 を AirPlay レシーバーが使っているため、5000 ではなく 5050 / 5051 を使っています。

## -2- リソースサーバーの起動

```sh
uv run python resource-server.py
```

ポート 5051 で起動します。

## -3- クライアントの起動

```sh
uv run python client.py
```

次のような出力になります：

```text
認可をリクエストしています: http://localhost:5050/authorize?client_id=abc&redirect_uri=http://localhost:3000/callback&state=xyz&code_challenge=123&code_challenge_method=plain
認可コードを受け取りました: d54cf5ec-12a2-4103-907f-027183665229
アクセストークン: ba0a046d-23c3-4f5b-a96c-e28752877e86
ユーザー情報の応答:
{'email': 'chris@example.com', 'name': 'Chris', 'sub': 'user123'}
```
