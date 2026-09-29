# サンプルの実行

## 環境のセットアップ

```sh
python -m venv venv
source ./venv/bin/activate
```

## サーバーの起動

```sh
uvicorn server:app --port 3000
```

## クライアントの実行

別のターミナルで次のコマンドを実行します：

```sh
python client.py
```

次のような出力になります：

```text
Available tools: ['book_trip']
[CLIENT] Received elicitation data: Not a member? Would you like to sign up?
[CLIENT]: Selecting alternative date: 2025-01-01
Result:  [BOOKED] Booked for 2025-01-02, welcome chris as a member!
````
