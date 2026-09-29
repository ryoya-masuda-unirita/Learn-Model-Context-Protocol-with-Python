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
使える tool: ['book_trip']
[CLIENT] elicitation のデータを受信しました: 2025-01-02 に予約できる旅行はありません。別の日付を試しますか？
[CLIENT]: 代わりの日付を選択します: 2025-01-01
結果:  [SUCCESS] 2025-01-01 で予約しました
```

コードの一部を見てみましょう。elicitation 用のクライアントのハンドラーです。ここではサーバーへの応答をハードコードしています：

```python
async def elicitation_callback_handler(context: RequestContext[ClientSession, None], params: ElicitRequestParams):
    print(f"[CLIENT] elicitation のデータを受信しました: {params.message}")
 
    # 1. 別の日付を選ぶのを断る
    # return ElicitResult(action="accept", content={
    #     "checkAlternative": False
    # }) # 予約は行われなかったと返るはず（動作確認済み）

    # 2. 予約をキャンセルする
    # return ElicitResult(action="decline"), 動作確認済み

    print("[CLIENT]: 代わりの日付を選択します: 2025-01-01")

    # 3. 別の日付 2025-01-01 を選び、予約が成立する
    return ElicitResult(action="accept", content={
         "checkAlternative": True,
         "alternativeDate": "2025-01-01"
    }) # 最初の 1月2日ではなく 1月1日で予約されるはず
```

ここでは、サーバーが受け付ける代わりの日付をあらかじめ入れた "accept" 応答をハードコードして返しています。ほかの応答パターンも用意しています。1) ユーザーが日付の選択を断る場合で、予約は行われなかったという応答になります。2) ユーザーがやり取り自体を取りやめる場合で、こちらも予約は行われません。

ハードコードではなくユーザーの入力で決まるようにこのコードを改良したり、別の応答を試して違いを確かめたりしてみてください。
