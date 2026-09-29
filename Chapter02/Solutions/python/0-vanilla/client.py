# 子プロセスを起動し、stdin 経由で情報を送る必要がある

import subprocess
import json

# 子プロセスを起動する
proc = subprocess.Popen(
    ['python3', 'server.py'],  # 起動する子スクリプトに置き換える
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

list_tools_message = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
};

message = 'hello\n'

def send_message(message):
    """子プロセスにメッセージを送る。"""
    print(f'[CLIENT] サーバーにメッセージを送信中... メッセージ: {message.strip()}')
    proc.stdin.write(message)
    proc.stdin.flush()

def serialize_message(message):
    """メッセージを JSON 形式にシリアライズする。"""
    return json.dumps(message) + '\n'

# 子プロセスにメッセージを送る
send_message(message)

# 子プロセスからの応答を読む
response = proc.stdout.readline()
print('[SERVER]:', response.strip())

# JSON-RPC メッセージを送る
send_message(serialize_message(list_tools_message))

response = proc.stdout.readline()
print('[SERVER]:', response.strip())

# 子プロセス（つまりサーバー）を終了させる
send_message('exit\n')

exit_code = proc.wait()
print(f"子プロセスが終了コード {exit_code} で終了しました")

proc.stdin.close()
proc.terminate()