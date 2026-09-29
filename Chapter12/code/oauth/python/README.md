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
python auth_server.py
```

## -2- リソースサーバーの起動

```sh
python resource_server.py
```

## -3- クライアントの起動

```sh
python client.py
```

次のような出力になります：

```text
Requesting authorization: http://localhost:5000/authorize?client_id=abc&redirect_uri=http://localhost:3000/callback&state=xyz&code_challenge=123&code_challenge_method=plain
Received authorization code: d54cf5ec-12a2-4103-907f-027183665229
Access token: ba0a046d-23c3-4f5b-a96c-e28752877e86
User info response:
{'email': 'chris@example.com', 'name': 'Chris', 'sub': 'user123'}
```
