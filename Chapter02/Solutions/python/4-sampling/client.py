"""サーバーからのサンプリングのリクエストに対応したクライアント。

別スレッドで子プロセスの stdout を監視し、サンプリングのリクエストはその場で処理する。
それ以外のメッセージはキューに入れ、メインスレッドで順に処理する。
"""
# 子プロセスを起動し、stdin 経由で情報を送る必要がある

import subprocess
import json
import threading
import queue
from typing import Any

from utils.messages import list_tools_message, initialize_message, initialized_message

message_queue: queue.Queue[str] = queue.Queue()

# 子プロセスを起動する
proc: subprocess.Popen[str] = subprocess.Popen(
    ['python3', 'server.py'],  # 起動する子スクリプトに置き換える
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

message: str = 'hello\n'

def is_sampling_message(message: dict[str, Any]) -> bool:
    """メッセージがサンプリングのメッセージかを判定する。

    Parameters
    ----------
    message : dict[str, Any]
        判定する JSON-RPC メッセージ。

    Returns
    -------
    bool
        method が "sampling" で始まれば True。
    """
    return message.get('method', '').startswith('sampling')

def is_notification_message(message: dict[str, Any]) -> bool:
    """メッセージが通知かを判定する。

    Parameters
    ----------
    message : dict[str, Any]
        判定する JSON-RPC メッセージ。

    Returns
    -------
    bool
        method が "notifications/" で始まれば True。
    """
    return message.get('method', '').startswith('notifications/')

def create_sampling_message(llm_response: str) -> dict[str, Any]:
    """商品用のサンプリングメッセージを作る。

    Parameters
    ----------
    llm_response : str
        LLM が生成したテキスト。

    Returns
    -------
    dict[str, Any]
        サーバーに返すサンプリングの応答メッセージ。
    """
    sampling_message = {
        "jsonrpc": "2.0",
        "result": {
            "content": {
                "text": llm_response
            }
        }
    }
    return sampling_message

def call_llm(message: str) -> str:
    """LLM の呼び出しを模擬する。

    Parameters
    ----------
    message : str
        LLM に渡すプロンプト。

    Returns
    -------
    str
        プロンプトの先頭に "LLM: " を付けた文字列。
    """
    return "LLM: " + message


def handle_sampling_message(message: dict[str, Any]) -> None:
    """サンプリングのメッセージを処理する。

    メッセージから内容を取り出して LLM に渡し、その応答をサーバーに返す。

    Parameters
    ----------
    message : dict[str, Any]
        サーバーから届いたサンプリングの JSON-RPC メッセージ。
    """
    print("[CLIENT] リクエストを完了するために LLM を呼び出します", message)
    # メッセージから内容を取り出し、LLM に送る

    content = message['params']['messages'][0]['content']['text']
    llm_response = call_llm(content)
    message = create_sampling_message(llm_response)
    send_message(serialize_message(message))
    # LLM を呼び出してリクエストを完了すべき

def listen_to_stdout() -> None:
    """子プロセスの stdout を監視し、メッセージを処理する。

    サンプリングのメッセージはその場で処理し、それ以外はキューに入れる。
    子プロセスの出力がなくなったら終了する。
    """
    # PIPE を指定しているので実行時は None にならないが、型の上では None もありうるため絞り込む
    assert proc.stdout is not None
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


def send_message(message: str) -> None:
    """子プロセスにメッセージを送る。

    Parameters
    ----------
    message : str
        送信するメッセージ。末尾に改行を含める必要がある。
    """
    assert proc.stdin is not None
    print_response(message, prefix='[CLIENT]: ')
    proc.stdin.write(message)
    proc.stdin.flush()

def serialize_message(message: dict[str, Any]) -> str:
    """メッセージを JSON 形式にシリアライズする。

    Parameters
    ----------
    message : dict[str, Any]
        シリアライズする JSON-RPC メッセージ。

    Returns
    -------
    str
        末尾に改行を付けた JSON 文字列。
    """
    return json.dumps(message) + '\n'

def print_response(response: str, prefix: str = "") -> None:
    """サーバーからの応答を表示する。

    JSON として解釈できれば整形して表示し、できなければそのまま表示する。

    Parameters
    ----------
    response : str
        表示する応答の文字列。
    prefix : str, optional
        応答の前に表示する接頭辞。デフォルトは空文字列。
    """
    try:
        parsed = json.loads(response)
        print(prefix,json.dumps(parsed, indent=2))
    except json.JSONDecodeError:
        print(prefix, response.strip())

def connect() -> None:
    """サーバーと initialize / initialized のハンドシェイクを行う。"""
    print("サーバーに接続しています...")
    # 1. capabilities を問い合わせる
    send_message(serialize_message(initialize_message))

    # 子プロセスからの応答を読む
    # response = proc.stdout.readline()
    response = message_queue.get()
    print_response(response, prefix='[SERVER]: \n')

    # 2. initialized 通知を送る
    send_message(serialize_message(initialized_message))

def send_simple_message(message: str) -> None:
    """テキストメッセージを送り、サーバーの応答を表示する。

    Parameters
    ----------
    message : str
        送信するメッセージ。末尾に改行を含める必要がある。
    """
    assert proc.stdout is not None
    # 子プロセスにシンプルなテキストメッセージを送る
    send_message(message)

    response = proc.stdout.readline()
    print_response(response, prefix='[SERVER]: \n')

def list_tools() -> list[dict[str, Any]]:
    """サーバーから tool の一覧を取得する。

    result を含む応答が届くまでに受け取った通知は、そのまま表示する。

    Returns
    -------
    list[dict[str, Any]]
        tool の定義（name、description、inputSchema を持つ辞書）のリスト。
    """
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
    # while を抜けるのは result を受け取って return したときだけなので、ここには到達しない
    raise AssertionError("到達しないはずのコードです")

def call_tool(tool_name: str, args: dict[str, Any]) -> list[dict[str, Any]]:
    """指定した tool を呼び出し、結果のコンテンツを返す。

    result を含む応答が届くまでに受け取った通知は、そのまま表示する。

    Parameters
    ----------
    tool_name : str
        呼び出す tool の名前。
    args : dict[str, Any]
        tool に渡す引数。

    Returns
    -------
    list[dict[str, Any]]
        tool の結果のコンテンツ（type と text を持つ辞書）のリスト。
    """
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
    # while を抜けるのは result を受け取って return したときだけなので、ここには到達しない
    raise AssertionError("到達しないはずのコードです")

def close_server() -> None:
    """サーバーに終了を指示し、子プロセスの終了を待つ。"""
    # exit を送らないとサーバーが終了せず、proc.wait() で待ち続けてしまう
    send_message('exit\n')

    exit_code = proc.wait()
    print(f"子プロセスが終了コード {exit_code} で終了しました")

tools: list[dict[str, Any]] = []

listener_thread: threading.Thread = threading.Thread(target=listen_to_stdout, daemon=True)
listener_thread.start()

def main() -> None:
    """接続、tool の一覧取得、最初の tool の呼び出し、サーバーの終了待ちを順に行う。"""
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
