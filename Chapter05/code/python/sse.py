"""Flask で Server-Sent Events (SSE) を送るサーバー。

/sse にアクセスすると、1秒ごとに現在時刻を5回送ってから接続を閉じる。
"""
from collections.abc import Iterator

from flask import Flask, Response
import time

app: Flask = Flask(__name__)


port: int = 8000

@app.route('/sse')
def sse() -> Response:
    """SSE のストリームを返す。

    Returns
    -------
    Response
        text/event-stream 形式でイベントを送り続けるレスポンス。
    """
    def generate() -> Iterator[str]:
        """1秒ごとに現在時刻のイベントを作る。

        Yields
        ------
        str
            SSE 形式（"data: ..." と空行）のイベント。
        """
        count = 0
        max = 5

        while True:
            # SSE のイベントは「data: 本文」の行と、終わりを示す空行（\n\n）でできている。
            # 空行を忘れると、クライアントはイベントの区切りがわからず受け取れない
            yield f"data: {time.ctime()}\n\n"
            count += 1
            if count >= max:
                yield f"data: {max} 件のメッセージを送信しました。接続を閉じます。\n\n"
                break
            time.sleep(1)

    # ジェネレーターを渡すと、Flask は yield されるたびにクライアントへ送る（全部できるまで待たない）。
    # text/event-stream は SSE であることを示す Content-Type。ブラウザの EventSource はこれでないと受け付けない
    return Response(generate(), mimetype='text/event-stream')

import json


if __name__ == '__main__':
    print(f"ポート {port} で SSE サーバーを起動しています...")
    app.run(port=port, debug=True)
