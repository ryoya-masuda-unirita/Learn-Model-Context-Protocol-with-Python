# 子プロセスを起動し、stdin 経由で情報を送る必要がある

import subprocess
import json
import threading
import queue

from utils.messages import list_tools_message, initialize_message, initialized_message

message_queue = queue.Queue()

# 子プロセスを起動する
proc = subprocess.Popen(
    ['python3', 'server.py'],  # 起動する子スクリプトに置き換える
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

message = 'hello\n'

def is_sampling_message(message):
    """メッセージがサンプリングのメッセージかを判定する。"""
    return message.get('method', '').startswith('sampling')

def is_notification_message(message):
    """メッセージが通知かを判定する。"""
    return message.get('method', '').startswith('notifications/')

def create_sampling_message(llm_response):
    """商品用のサンプリングメッセージを作る。"""
    sampling_message = {
        "jsonrpc": "2.0",
        "result": {
            "content": {
                "text": llm_response
            }
        }
    }
    return sampling_message

def call_llm(message):
    return "LLM: " + message


def handle_sampling_message(message):
    """サンプリングのメッセージを処理する。"""
    print("[CLIENT] リクエストを完了するために LLM を呼び出します", message)
    # メッセージから内容を取り出し、LLM に送る

    content = message['params']['messages'][0]['content']['text']
    llm_response = call_llm(content)
    message = create_sampling_message(llm_response)
    send_message(serialize_message(message))
    # LLM を呼び出してリクエストを完了すべき

def listen_to_stdout():
    """子プロセスの stdout を監視し、メッセージを処理する。"""
    while True:
        response = proc.stdout.readline()
        if not response:
            break  # 出力がなくなったら終了する

        try:
            parsed_response = json.loads(response)
            if is_sampling_message(parsed_response):
                handle_sampling_message(parsed_response)
                # サンプリングのメッセージならここで処理する
            else:
                # 後続の処理のためにキューに入れる
                message_queue.put(response.strip())
        except json.JSONDecodeError:
            # 応答が JSON でなければ、そのまま表示する
            print("[THREAD] JSON ではない応答を受信しました:", response.strip())
            # print_response(response, prefix='[THREAD]: \n')


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
    # response = proc.stdout.readline()
    response = message_queue.get()
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

    has_result = False
    while not has_result:
        # response = proc.stdout.readline()
        response = message_queue.get()
        # メッセージに result 属性があれば、ループを抜ける

        parsed_response = json.loads(response)
        if 'result' in parsed_response:
            has_result = True
            return parsed_response['result']['tools']
        else:
            # これは通知なので表示する
            print_response(response, prefix=f'[SERVER] {parsed_response["method"]}: \n')

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

    has_result = False
    send_message(serialize_message(tool_message))

    while not has_result:
        response = message_queue.get()
        # response = proc.stdout.readline()
        parsed_response = json.loads(response)
        if 'result' in parsed_response:
            has_result = True
            return parsed_response["result"]["properties"]["content"]["items"]
        else:
            # これは通知なので表示する
            print_response(response, prefix=f'[SERVER] {parsed_response["method"]}: \n')

def close_server():
    # send_message('exit\n')

    exit_code = proc.wait()
    print(f"子プロセスが終了コード {exit_code} で終了しました")

tools = []

listener_thread = threading.Thread(target=listen_to_stdout, daemon=True)
listener_thread.start()

def main():
    connect()

    # サンプリングのメッセージは、ここでいつでも送られてくる可能性がある

    tool_response = list_tools()
    tools.extend(tool_response)

    print("使える tool:", tools)

    tool = tools[0]

    tool_call_response = call_tool(tool["name"],{"args1": "こんにちは"})
    for content in tool_call_response:
        print_response(content['text'], prefix='[SERVER] tool の応答: \n')

    # tool を呼び出すには、名前と引数が必要
    close_server()

main()


# TODO: 通知に対応する。tool の呼び出しや一覧取得のときにループするか、非同期の仕組みを使う
