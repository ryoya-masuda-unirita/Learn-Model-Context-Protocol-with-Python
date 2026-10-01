# サンプルの実行

## 環境のセットアップ

[uv](https://docs.astral.sh/uv/) で依存関係をインストールします（初回のみ）。リポジトリ内のどのディレクトリで実行しても、リポジトリ直下の `.venv` にインストールされます：

```bash
uv sync
```

以降のコマンドは `uv run` を付けて実行します。仮想環境を有効化する必要はありません。

## サーバーの起動

```sh
uv run uvicorn server:app --port 3000
```

## クライアントの実行

別のターミナルで次のコマンドを実行します：

```sh
uv run python client.py
```

次のような出力になります：

```text
使える tool: ['book_trip']
[CLIENT] elicitation のデータを受信しました: 会員ではありませんか？ 会員登録しますか？
[CLIENT]: 会員登録します: chris（chris@example.com）
結果:  [BOOKED] 2025-01-02 で予約しました。chris さん、会員登録ありがとうございます！
````
