# OAuth サンプルの実行


## -0- セットアップ

仮想環境を作成して有効化します。

```sh
python -m venv venv
source venv/bin/activate
```

```sh
pip install flask requests
```

## -1- 認可サーバーの起動

```sh
python auth-server.py
```

ポート 5050 で起動します。

> macOS ではポート 5000 を AirPlay レシーバーが使っているため、5000 ではなく 5050 / 5051 を使っています。

## -2- リソースサーバーの起動

```sh
python resource-server.py
```

ポート 5051 で起動します。

## -3- クライアントの起動

```sh
python client.py
```

次のような出力になります：

```text
認可をリクエストしています: http://localhost:5050/authorize?client_id=abc&redirect_uri=http://localhost:3000/callback&state=xyz&code_challenge=123&code_challenge_method=plain
認可コードを受け取りました: d54cf5ec-12a2-4103-907f-027183665229
アクセストークン: ba0a046d-23c3-4f5b-a96c-e28752877e86
ユーザー情報の応答:
{'email': 'chris@example.com', 'name': 'Chris', 'sub': 'user123'}
```
