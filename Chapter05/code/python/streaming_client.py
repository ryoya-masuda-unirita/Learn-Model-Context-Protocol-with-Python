"""ストリーミングサーバー（streaming.py）からメッセージを受け取って表示するクライアント。"""
import requests

port: int = 8000

def consume_stream() -> None:
    """/stream に接続し、受け取ったメッセージを1行ずつ表示する。"""
    # stream=True にしないと、requests はレスポンスを最後まで受け取ってから返すので、届いた順に表示できない
    response = requests.get(f'http://localhost:{port}/stream', stream=True)
    for line in response.iter_lines():
        if line:
            print(line.decode('utf-8'))
consume_stream()
