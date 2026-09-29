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
使える tool: ['book_trip']
[CLIENT] elicitation のデータを受信しました: 会員ではありませんか？ 会員登録しますか？
[CLIENT]: 代わりの日付を選択します: 2025-01-01
結果:  [BOOKED] 2025-01-02 で予約しました。chris さん、会員登録ありがとうございます！
````
