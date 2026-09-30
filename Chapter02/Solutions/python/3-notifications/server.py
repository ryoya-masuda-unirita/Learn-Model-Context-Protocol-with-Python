"""応答の前に進捗の通知（notifications/progress）を送るサーバー。

初期化が終わるまでは、initialize と notifications/initialized 以外のメソッドを受け付けない。
"""
import sys
import json
from typing import Any

from utils.messages import initializeResponse, progress_notification

# initialize → notifications/initialized のハンドシェイクが終わったかどうか
initialized: bool = False

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
            method: str = json_message.get('method', '')

            # ハンドシェイクが終わるまでは、initialize と notifications/initialized 以外を受け付けない
            if not initialized:
                if method != "initialize" and method != "notifications/initialized":
                    print(f"サーバーが初期化されていません。先に 'initialized' 通知を送ってください。送られたメソッド: {method}")
                    sys.stdout.flush()
                    continue

            match method:
                case "notifications/initialized":
                    # 通知（id を持たないメッセージ）なので、応答は返さない
                    # print("サーバーの初期化に成功しました。")
                    sys.stdout.flush()
                    initialized = True
                    break
                case "initialize":
                    # サーバーの capabilities を返す。ここではまだ initialized にせず、クライアントからの initialized 通知を待つ
                    print(json.dumps(initializeResponse))
                    sys.stdout.flush()
                    # initialized = True
                    break
                     # capabilities を返すべき
                case "tools/call":
                    tool_name: str = json_message['params']['name']
                    args: dict[str, Any] = json_message['params']['args']

                    # 応答（result）の前に進捗の通知を2回送る。
                    # 通知と応答は同じ stdout に流れるので、クライアントは通知を読み飛ばして応答を待つ必要がある
                    print(json.dumps(progress_notification))
                    sys.stdout.flush()

                    print(json.dumps(progress_notification))
                    sys.stdout.flush()

                    # TODO: tool 呼び出しへの応答を作る（つまり、正しい tool を呼び出す）
                    # 本来の MCP では、引数のキーは "arguments"、結果は {"content": [...]} の形。ここでは独自の形に簡略化している
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

                    # 先に進捗の通知を送り、その後で応答を返す
                    print(json.dumps(progress_notification))
                    sys.stdout.flush()

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
        # "exit" はこのサンプル独自の終了コマンド（MCP の仕様にはない）。実際の stdio サーバーは stdin が閉じられたら終了する
        elif message == "exit":
            print("サーバーを終了します。")
            sys.stdout.flush()
            sys.exit(0)
        else:
            print(f"不明なメッセージです: {message}")
