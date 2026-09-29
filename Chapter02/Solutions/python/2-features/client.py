# 子プロセスを起動し、stdin 経由で情報を送る必要がある

import subprocess
import json

from utils.messages import list_tools_message, initialize_message, initialized_message

# 子プロセスを起動する
proc = subprocess.Popen(
    ['python3', 'server.py'],  # 起動する子スクリプトに置き換える
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

message = 'hello\n'

def send_message(message):
    """子プロセスにメッセージを送る。"""
    print_response(message, prefix='[CLIENT]: ')
    proc.stdin.write(message)
    proc.stdin.flush()

def serialize_message(message):
    """メッセージを JSON 形式にシリアライズする。"""
    return json.dumps(message) + '\n'

def print_response(response, prefix = ""):
    """サーバーからの応答を表示する。"""
    try:
        parsed = json.loads(response)
        print(prefix,json.dumps(parsed, indent=2))
    except json.JSONDecodeError:
        print(prefix, response.strip())

def connect():
    print("サーバーに接続しています...")
    # 1. capabilities を問い合わせる
    send_message(serialize_message(initialize_message))

    # 子プロセスからの応答を読む
    response = proc.stdout.readline()
    print_response(response, prefix='[SERVER]: \n')

    # 2. initialized 通知を送る
    send_message(serialize_message(initialized_message))

def send_simple_message(message):
    # 子プロセスにシンプルなテキストメッセージを送る
    send_message(message)

    response = proc.stdout.readline()
    print_response(response, prefix='[SERVER]: \n')

def list_tools():
    # 3. tool の一覧を取得するメッセージを送る
    # JSON-RPC メッセージを送る
    send_message(serialize_message(list_tools_message))

    response = proc.stdout.readline()
    return json.loads(response)['result']['tools']

def call_tool(tool_name, args):
    # 4. tool を呼び出す
    # JSON-RPC メッセージを送る

    tool_message = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "args": args
        },
        "id": 1
    }
    send_message(serialize_message(tool_message))
    response = proc.stdout.readline()
    return json.loads(response)["result"]["properties"]["content"]["items"]

def close_server():
    send_message('exit\n')

    exit_code = proc.wait()
    print(f"子プロセスが終了コード {exit_code} で終了しました")

tools = []

def main():
    connect()
    tool_response = list_tools()
    tools.extend(tool_response)

    print("使える tool:", tools)

    tool = tools[0]

    tool_call_response = call_tool(tool["name"],{"args1": "こんにちは"})
    for content in tool_call_response:
        print_response(content['text'], prefix='[SERVER] tool の応答: \n')
    # print_response(tool_call_response['result'], prefix='[SERVER]: \n')

    # tool を呼び出すには、名前と引数が必要
    close_server()

main()

