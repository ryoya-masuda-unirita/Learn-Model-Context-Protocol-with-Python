# このサンプルの実行

このサンプルには2種類のストリーミングサーバーがあります：

- SSE (Server-Sent Events)
- Streaming HTTP

## 仮想環境の作成

```bash
python -m venv venv
```

## 仮想環境の有効化

**Windows の場合**

```bash
.\venv\Scripts\activate
```

**macOS / Linux の場合**


```bash
source venv/bin/activate
```

## 依存関係のインストール

```bash
pip install Flask requests
```

## SSE サンプルの実行

サーバーを起動します：

```bash
python sse.py
```

クライアントが接続すると、サーバーのコンソールに次のように表示されます：

```text
ポート 8000 で SSE サーバーを起動しています...
```

別のターミナルでクライアントを起動します：

```bash
python sse_client.py 
```

クライアントのコンソールには次のような出力が表示されます：

```text
SSE を受信: data: Sun Jun  1 18:48:42 2025
SSE を受信: data: Sun Jun  1 18:48:43 2025
SSE を受信: data: Sun Jun  1 18:48:44 2025
SSE を受信: data: Sun Jun  1 18:48:45 2025
SSE を受信: data: Sun Jun  1 18:48:46 2025
SSE を受信: data: 5 件のメッセージを送信しました。接続を閉じます。
```

## Streaming HTTP サンプルの実行

サーバーを起動します：

```bash
python streaming.py
```

クライアントが接続すると、サーバーのコンソールに次のように表示されます：

```text
ポート 8000 でストリーミングサーバーを起動しています...
```

別のターミナルでクライアントを起動します：

```bash
python streaming_client.py
```
クライアントのコンソールには次のような出力が表示されます：

```text
{'message': 'こんにちは、世界！'}
{'message': 'こんにちは、世界！'}
{'message': 'こんにちは、世界！'}
{'message': 'こんにちは、世界！'}
{'message': 'こんにちは、世界！'}
5 件のメッセージに達しました。接続を閉じます。
```
