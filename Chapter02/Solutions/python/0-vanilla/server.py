"""stdin からメッセージを受け取り、stdout に応答を返す最小限のサーバー。

"hello" への応答、JSON-RPC の tools/list への応答、"exit" での終了に対応する。
"""
import sys
import json
from typing import Any

while True:
    for line in sys.stdin:
        message: str = line.strip()
        if message == "hello":
            print("こんにちは")
            sys.stdout.flush()  # 出力をすぐに送る
        elif message.startswith('{"jsonrpc":'):
            json_message: dict[str, Any] = json.loads(message)
            match json_message['method']:
                case "tools/list":
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
        elif message == "exit":
            print("サーバーを終了します。")
            sys.stdout.flush()
            sys.exit(0)
        else:
            print(f"不明なメッセージです: {message}")
