from flask import Flask, Response
import time

port = 8000

app = Flask(__name__)
@app.route('/stream')
def stream():
    def generate():
        count = 0
        max_count = 5
        data = {'message': 'こんにちは、世界！'}
        while True:
            yield f"{data}\n"
            count += 1
            if count >= max_count:
                yield f"{max_count} 件のメッセージに達しました。接続を閉じます。\n"
                break
            time.sleep(1)
    
    return Response(generate(), mimetype='application/json')

if __name__ == '__main__':
    print(f"ポート {port} でストリーミングサーバーを起動しています...")
    app.run(port=port)
