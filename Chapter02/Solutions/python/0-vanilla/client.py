"""サーバーを子プロセスとして起動し、stdin / stdout でメッセージをやり取りするクライアント。

MCP の仕組みを理解するため、SDK を使わずに最小限のやり取りを行う。
"""
# 子プロセスを起動し、stdin 経由で情報を送る必要がある

import subprocess
import json
from typing import Any

# 子プロセスを起動する
# stdin / stdout をパイプでつなぐ。これが MCP の stdio トランスポートの基本形
proc: subprocess.Popen[str] = subprocess.Popen(
    ['python3', 'server.py'],  # 起動する子スクリプトに置き換える
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True  # bytes ではなく str でやり取りする
)
# PIPE を指定しているので実行時は None にならないが、型の上では None もありうるため絞り込む
assert proc.stdin is not None and proc.stdout is not None

# JSON-RPC 2.0 のリクエスト。id を付けると、応答が必要な「リクエスト」になる
list_tools_message: dict[str, Any] = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
};

message: str = 'hello\n'

def send_message(message: str) -> None:
    """子プロセスにメッセージを送る。

    Parameters
    ----------
    message : str
        送信するメッセージ。末尾に改行を含める必要がある。
    """
    assert proc.stdin is not None
    print(f'[CLIENT] サーバーにメッセージを送信中... メッセージ: {message.strip()}')
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

# 子プロセスにメッセージを送る
send_message(message)

# 子プロセスからの応答を読む
# サーバーは1行で応答するので、1行だけ読む。応答が届くまでここで待つ
response: str = proc.stdout.readline()
print('[SERVER]:', response.strip())

# JSON-RPC メッセージを送る
send_message(serialize_message(list_tools_message))

response = proc.stdout.readline()
print('[SERVER]:', response.strip())

# 子プロセス（つまりサーバー）を終了させる
# "exit" はこのサンプル独自の終了コマンド（MCP の仕様にはない）
send_message('exit\n')

exit_code: int = proc.wait()
print(f"子プロセスが終了コード {exit_code} で終了しました")

proc.stdin.close()
proc.terminate()