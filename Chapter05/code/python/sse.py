from flask import Flask, Response
import time

app = Flask(__name__)


port = 8000

@app.route('/sse')
def sse():
    def generate():

        count = 0
        max = 5

        while True:
            yield f"data: {time.ctime()}\n\n"
            count += 1
            if count >= max:
                yield f"data: {max} 件のメッセージを送信しました。接続を閉じます。\n\n"
                break
            time.sleep(1)
    
    return Response(generate(), mimetype='text/event-stream')

import json


if __name__ == '__main__':
    print(f"ポート {port} で SSE サーバーを起動しています...")
    app.run(port=port, debug=True)
