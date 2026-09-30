"""stdin からメッセージを受け取り、stdout に応答を返す最小限のサーバー。

"hello" への応答、JSON-RPC の tools/list への応答、"exit" での終了に対応する。
"""
import sys
import json
from typing import Any

# stdio トランスポートでは「1行 = 1メッセージ」。stdin を1行ずつ読んで処理する。
# 各 case の break で for を抜けても、外側の while True で再び stdin を読み始めるので処理は続く
while True:
    for line in sys.stdin:
        message: str = line.strip()
        if message == "hello":
            print("こんにちは")
            # stdout がパイプだとバッファリングされるので、flush しないとクライアントの readline() が待ち続ける
            sys.stdout.flush()
        # クライアントは json.dumps で送るので、JSON-RPC のメッセージは必ず '{"jsonrpc":' で始まる
        elif message.startswith('{"jsonrpc":'):
            json_message: dict[str, Any] = json.loads(message)
            # method の値で処理を振り分ける（match 文は Python 3.10 以降）
            match json_message['method']:
                case "tools/list":
                    # 応答にはリクエストと同じ id を入れる。クライアントはこの id で、どのリクエストへの応答かを対応付ける
                    # 本来の MCP では result は {"tools": [...]} の形。ここでは仕組みを見るため、tool の名前だけを返している
                    response: dict[str, Any] = {
                        "jsonrpc": "2.0",
                        "id": json_message["id"],
                        "result": ["tool1", "tool2"]
                    }
                    print(json.dumps(response))
                    sys.stdout.flush()
                    break
                case _:
                    print(f"不明なメソッドです: {json_message['method']}")
                    sys.stdout.flush()
                    break
        # "exit" はこのサンプル独自の終了コマンド（MCP の仕様にはない）。実際の stdio サーバーは stdin が閉じられたら終了する
        elif message == "exit":
            print("サーバーを終了します。")
            sys.stdout.flush()
            sys.exit(0)
        else:
            print(f"不明なメッセージです: {message}")
