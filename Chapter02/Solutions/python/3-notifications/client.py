"""サーバーからの通知（notifications）に対応したクライアント。

応答を待つ間に通知が届いても、result を含む応答が来るまで読み続ける。
"""
# 子プロセスを起動し、stdin 経由で情報を送る必要がある

import subprocess
import json
from typing import Any

from utils.messages import list_tools_message, initialize_message, initialized_message

# 子プロセスを起動する
proc: subprocess.Popen[str] = subprocess.Popen(
    ['python3', 'server.py'],  # 起動する子スクリプトに置き換える
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

message: str = 'hello\n'

def send_message(message: str) -> None:
    """子プロセスにメッセージを送る。

    Parameters
    ----------
    message : str
        送信するメッセージ。末尾に改行を含める必要がある。
    """
    # PIPE を指定しているので実行時は None にならないが、型の上では None もありうるため絞り込む
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
    assert proc.stdout is not None
    print("サーバーに接続しています...")
    # 1. capabilities を問い合わせる
    send_message(serialize_message(initialize_message))

    # 子プロセスからの応答を読む
    response = proc.stdout.readline()
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
    assert proc.stdout is not None
    # 3. tool の一覧を取得するメッセージを送る
    # JSON-RPC メッセージを送る
    send_message(serialize_message(list_tools_message))

    has_result = False
    while not has_result:
        response = proc.stdout.readline()
        # メッセージに result 属性があれば、ループを抜ける

        parsed_response = json.loads(response)
        if 'result' in parsed_response:
            has_result = True
            return parsed_response['result']['tools']
        else:
            # これは通知なので表示する
            print_response(response, prefix='[SERVER] 通知: \n')
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
    assert proc.stdout is not None
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
        response = proc.stdout.readline()
        parsed_response = json.loads(response)
        if 'result' in parsed_response:
            has_result = True
            return parsed_response["result"]["properties"]["content"]["items"]
        else:
            # これは通知なので表示する
            print_response(response, prefix='[SERVER] 通知: \n')
    # while を抜けるのは result を受け取って return したときだけなので、ここには到達しない
    raise AssertionError("到達しないはずのコードです")

def close_server() -> None:
    """サーバーに終了を指示し、子プロセスの終了を待つ。"""
    send_message('exit\n')

    exit_code = proc.wait()
    print(f"子プロセスが終了コード {exit_code} で終了しました")

tools: list[dict[str, Any]] = []

def main() -> None:
    """接続、tool の一覧取得、最初の tool の呼び出し、サーバーの終了を順に行う。"""
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


# TODO: 通知に対応する。tool の呼び出しや一覧取得のときにループするか、非同期の仕組みを使う
