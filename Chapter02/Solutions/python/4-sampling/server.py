import sys
import json
import queue
import threading
import random

from utils.messages import initializeResponse, progress_notification


initialized = False

product = {
    "id": "12345",
    "name": "サンプル商品",
    "price": 19.99,
    "keywords": ["サンプル", "商品", "例"]
}

class ProductStore:
    def __init__(self):
        self.started = False
        self.listeners = {}
        # 5秒ごとに商品をキューに追加するタイマーを作る

    def add_product(self):
        """ストアに商品を追加し、リスナーに通知する。"""
        product = {
            "id": str(random.randint(10000, 99999)),
            "name": f"商品 {random.randint(1, 100)}",
            "price": round(random.uniform(10.0, 100.0), 2),
            "keywords": [f"キーワード{random.randint(1, 5)}" for _ in range(random.randint(1, 3))]
        }
        self.dispatch_message("new_product", product)

    def start_product_queue_timer(self):
        """5秒ごとに商品をキューに追加するタイマーを開始する。"""
        def schedule_next():
            delay = random.uniform(1, 2)
            self.product_timer = threading.Timer(delay, self.add_product)
            self.product_timer.start()

        def add_twice():
            schedule_next()
            schedule_next()

        add_twice()

    def add_listener(self, message, callback):
        if not self.started:
            self.started = True
            self.start_product_queue_timer()
        """商品の更新を受け取るリスナーを追加する。"""
        # 実際のアプリケーションでは、新しい商品が追加されたときに呼ばれるコールバックとして登録する
        callbacks = self.listeners.get(message, [])
        callbacks.append(callback)
        self.listeners[message] = callbacks

    def dispatch_message(self, message, payload):
        """登録されているすべてのリスナーにメッセージを送る。"""
        callbacks = self.listeners.get(message, [])
        for callback in callbacks:
            callback(payload)

def create_sampling_message(product):
    sampling_message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "sampling/createMessage",
        "params": {
            "messages": [{
                "role": "system",
                "content": {
                    "type": "text",
                    "text": f"新しい商品が入荷しました: {product['name']}（ID: {product['id']}、価格: {product['price']}）。キーワード: {', '.join(product['keywords'])}"
                }
            }],
            "systemPrompt": "あなたは商品説明の作成を手伝う、親切なアシスタントです",
            "includeContext": "thisServer",
            "maxTokens": 300
        }
    }
    return sampling_message

store = ProductStore()
store.add_listener("new_product", lambda product: print(json.dumps(create_sampling_message(product))) and sys.stdout.flush())

def handle_sampling_response(response):
    content = response['result']['content']['text']
    print("[SERVER] [サンプリングの応答を受信しました]:", content)
    sys.stdout.flush()
    # TODO: 応答を使ってストアを更新するなど、必要な処理を行う

while True:
    for line in sys.stdin:
        message = line.strip()
        if message == "hello":
            print("こんにちは")
            sys.stdout.flush()  # 出力をすぐに送る
        elif message.startswith('{"jsonrpc":'):
            json_message = json.loads(message)
            method = json_message.get('method', '')

            if not initialized:
                if method != "initialize" and method != "notifications/initialized":
                    print(f"サーバーが初期化されていません。先に 'initialized' 通知を送ってください。送られたメソッド: {method}")
                    sys.stdout.flush()
                    continue



            match method:
                case "notifications/initialized":
                    # print("サーバーの初期化に成功しました。")
                    sys.stdout.flush()
                    initialized = True
                    break
                case "initialize":
                    print(json.dumps(initializeResponse))
                    sys.stdout.flush()
                    # initialized = True
                    break
                     # capabilities を返すべき
                case "tools/call":
                    tool_name = json_message['params']['name']
                    args = json_message['params']['args']

                    print(json.dumps(create_sampling_message(product)))
                    sys.stdout.flush()

                    print(json.dumps(progress_notification))
                    sys.stdout.flush()

                    print(json.dumps(progress_notification))
                    sys.stdout.flush()

                    # TODO: tool 呼び出しへの応答を作る（つまり、正しい tool を呼び出す）
                    response = {
                        "jsonrpc": "2.0",
                        "id": json_message["id"],
                        "result": {
                            "properties": {
                                "content": {
                                    "description": "コンテンツの説明",
                                    "items": [
                                        { "type": "text", "text": f"tool {tool_name} を引数 {args} で呼び出しました" }
                                    ]
                                }
                            }
                        }
                    }
                    print(json.dumps(response))
                    sys.stdout.flush()
                    break
                case "tools/list":

                    # 先に進捗の通知を送り、その後で応答を返す
                    print(json.dumps(progress_notification))
                    sys.stdout.flush()

                    response = {
                        "jsonrpc": "2.0",
                        "id": json_message["id"],
                        "result": {
                            "tools": [
                                {
                                    "name": "example_tool",
                                    "description": "何かを行うサンプルの tool。",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "arg1": {
                                                "type": "string",
                                                "description": "サンプルの引数。"
                                            }
                                        },
                                        "required": ["arg1"]
                                    }
                                }
                            ]
                        }
                    }
                    print(json.dumps(response))
                    sys.stdout.flush()
                    break
                case _:
                    # print(f"不明なメソッドです: {method}")
                    # sys.stdout.flush()
                    if json_message['result']:
                        handle_sampling_response(json_message)
                    # サンプリングの応答なので処理する（つまり、ストアを更新する）
                    else:
                        print(f"不明なメソッドです: {json_message['method']}")
                        sys.stdout.flush()
                    break
        elif message == "exit":
            print("サーバーを終了します。")
            sys.stdout.flush()
            sys.exit(0)
        else:
            print(f"不明なメッセージです: {message}")
