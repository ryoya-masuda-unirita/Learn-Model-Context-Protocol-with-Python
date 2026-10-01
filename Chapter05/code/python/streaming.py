"""Flask で HTTP ストリーミングのレスポンスを返すサーバー。

/stream にアクセスすると、1秒ごとにメッセージを5回送ってから接続を閉じる。
"""
from collections.abc import Iterator

from flask import Flask, Response
import json
import time

port: int = 8000

app: Flask = Flask(__name__)
@app.route('/stream')
def stream() -> Response:
    """ストリーミングのレスポンスを返す。

    Returns
    -------
    Response
        メッセージを1行ずつ送り続けるレスポンス。
    """
    def generate() -> Iterator[str]:
        """1秒ごとにメッセージを作る。

        Yields
        ------
        str
            改行で終わる1行分のメッセージ。
        """
        count = 0
        max_count = 5
        data = {'message': 'こんにちは、世界！'}
        while True:
            # 1行に JSON を1つずつ送る（stdio の「1行 = 1メッセージ」と同じ考え方）。クライアントは改行で区切って読める。
            # f"{data}" だと Python の辞書の表記（シングルクォート）になり、JSON として読めない
            yield json.dumps(data, ensure_ascii=False) + "\n"
            count += 1
            if count >= max_count:
                yield f"{max_count} 件のメッセージに達しました。接続を閉じます。\n"
                break
            time.sleep(1)

    # SSE と違い、data: や空行の決まりはない。届いたバイト列をどう区切るかは、サーバーとクライアントの取り決め次第
    return Response(generate(), mimetype='application/json')

if __name__ == '__main__':
    print(f"ポート {port} でストリーミングサーバーを起動しています...")
    app.run(port=port)
