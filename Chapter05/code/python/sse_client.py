"""SSE サーバー（sse.py）からイベントを受け取って表示するクライアント。"""
import requests

def consume_sse() -> None:
    """/sse に接続し、受け取ったイベントを1行ずつ表示する。"""
    response = requests.get('http://localhost:8000/sse', stream=True)
    for line in response.iter_lines():
        if line:
            print('SSE を受信:', line.decode('utf-8'))
consume_sse()
