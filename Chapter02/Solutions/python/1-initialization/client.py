"""initialize / initialized のハンドシェイクを行ってから tool の一覧を取得するクライアント。

サーバーを子プロセスとして起動し、stdin / stdout で JSON-RPC メッセージをやり取りする。
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

def list_tools() -> None:
    """サーバーに tool の一覧を問い合わせ、応答を表示する。"""
    assert proc.stdout is not None
    # 3. tool の一覧を取得するメッセージを送る
    # JSON-RPC メッセージを送る
    send_message(serialize_message(list_tools_message))

    response = proc.stdout.readline()
    print_response(response, prefix='[SERVER]: \n')

def close_server() -> None:
    """サーバーに終了を指示し、子プロセスの終了を待つ。"""
    send_message('exit\n')

    exit_code = proc.wait()
    print(f"子プロセスが終了コード {exit_code} で終了しました")

def main() -> None:
    """接続、tool の一覧取得、サーバーの終了を順に行う。"""
    connect()
    list_tools()
    close_server()

main()

