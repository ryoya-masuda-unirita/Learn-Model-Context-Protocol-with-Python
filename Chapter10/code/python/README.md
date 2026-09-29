# コードの実行

このサンプルでは Elicitation の使い方を示します。

## 環境のセットアップ

```sh
python -m venv venv
source ./venv/bin/activate
```

## サーバーの実行

```sh
uvicorn server:app
```

次のように表示されます：

```text
INFO:     Started server process [5016]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

ポート 8000 でサーバーが起動します。

## VS Code でサーバーを試す

*mcp.json* に次のようなエントリを追加します：

```json
"server": {
    "type": "sse",
    "url": "http://localhost:8000/sse"
    
}
```

サーバーを起動したら、チャットで次のプロンプトを入力してみてください：

```text
Book trip on 2025-02-01
```

このプロンプトで Elicitation のシナリオが始まり、追加の入力を求められます。"2025-01-01" と入力すると予約が成功します：

![VS Code での Elicitation の例](../../assets/elicitation.png)

## クライアントの実行

次のコマンドを実行します：

```sh
python client.py
```

クライアントが起動し、次のような出力になります：

```text
Available tools: ['book_trip']
[CLIENT] Received elicitation data: No trips available on 2025-01-02. Would you like to try another date?
[CLIENT]: Selecting alternative date: 2025-01-01
Result:  [SUCCESS] Booked for 2025-01-01
```

コードの一部を見てみましょう。elicitation 用のクライアントのハンドラーです。ここではサーバーへの応答をハードコードしています：

```python
async def elicitation_callback_handler(context: RequestContext[ClientSession, None], params: ElicitRequestParams):
    print(f"[CLIENT] Received elicitation data: {params.message}")
 
    # 1. refuses no select other date
    # return ElicitResult(action="accept", content={
    #     "checkAlternative": False
    # }) # should say no booking made, WORKS

    # 2. cancels booking
    # return ElicitResult(action="decline"), WORKS

    print("[CLIENT]: Selecting alternative date: 2025-01-01")

    # 3. opts to select another date, 2025-01-01 which leads to a booking
    return ElicitResult(action="accept", content={
         "checkAlternative": True,
         "alternativeDate": "2025-01-01"
    }) # should book 1 jan instead of initial 2nd Jan
```

ここでは、サーバーが受け付ける代わりの日付をあらかじめ入れた "accept" 応答をハードコードして返しています。ほかの応答パターンも用意しています。1) ユーザーが日付の選択を断る場合で、予約は行われなかったという応答になります。2) ユーザーがやり取り自体を取りやめる場合で、こちらも予約は行われません。

ハードコードではなくユーザーの入力で決まるようにこのコードを改良したり、別の応答を試して違いを確かめたりしてみてください。
