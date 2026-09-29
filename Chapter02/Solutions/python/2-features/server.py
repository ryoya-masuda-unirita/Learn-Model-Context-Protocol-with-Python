"""tool の一覧取得と tool の呼び出しに対応したサーバー。

初期化が終わるまでは、initialize と notifications/initialized 以外のメソッドを受け付けない。
"""
import sys
import json
from typing import Any

from utils.messages import initializeResponse

initialized: bool = False

def create_notification() -> dict[str, Any]:
    """通知メッセージを作る。

    Returns
    -------
    dict[str, Any]
        notifications/initialized の JSON-RPC 通知メッセージ。
    """
    return {
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
        "params": {}
    }

while True:
    for line in sys.stdin:
        message: str = line.strip()
        if message == "hello":
            print("こんにちは")
            sys.stdout.flush()  # 出力をすぐに送る
        elif message.startswith('{"jsonrpc":'):
            json_message: dict[str, Any] = json.loads(message)
            method: str = json_message.get('method', '')

            if not initialized:
                if method != "initialize" and method != "notifications/initialized":
                    print(f"サーバーが初期化されていません。先に 'initialized' 通知を送ってください。送られたメソッド: {method}")
                    sys.stdout.flush()
                    continue

            match method:
                case "notifications/initialized":
                    # print("サーバーの初期化に成功しました。")
                    sys.stdout.flush()
                    initialized = True
                    break
                case "initialize":
                    print(json.dumps(initializeResponse))
                    sys.stdout.flush()
                    # initialized = True
                    break
                     # capabilities を返すべき
                case "tools/call":



                    tool_name: str = json_message['params']['name']
                    args: dict[str, Any] = json_message['params']['args']
                    # TODO: tool 呼び出しへの応答を作る（つまり、正しい tool を呼び出す）
                    response: dict[str, Any] = {
                        "jsonrpc": "2.0",
                        "id": json_message["id"],
                        "result": {
                            "properties": {
                                "content": {
                                    "description": "コンテンツの説明",
                                    "items": [
                                        { "type": "text", "text": f"tool {tool_name} を引数 {args} で呼び出しました" }
                                    ]
                                }
                            }
                        }
                    }
                    print(json.dumps(response))
                    sys.stdout.flush()
                    break
                case "tools/list":

                    response = {
                        "jsonrpc": "2.0",
                        "id": json_message["id"],
                        "result": {
                            "tools": [
                                {
                                    "name": "example_tool",
                                    "description": "何かを行うサンプルの tool。",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "arg1": {
                                                "type": "string",
                                                "description": "サンプルの引数。"
                                            }
                                        },
                                        "required": ["arg1"]
                                    }
                                }
                            ]
                        }
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
