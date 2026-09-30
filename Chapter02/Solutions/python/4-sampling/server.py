"""クライアントにサンプリングを依頼するサーバー。

新しい商品が追加されると、その商品説明の生成をクライアントの LLM に依頼する
（sampling/createMessage を送る）。
"""
import sys
import json
import queue
import threading
import random
from collections.abc import Callable
from typing import Any

from utils.messages import initializeResponse, progress_notification


# initialize → notifications/initialized のハンドシェイクが終わったかどうか
initialized: bool = False

product: dict[str, Any] = {
    "id": "12345",
    "name": "サンプル商品",
    "price": 19.99,
    "keywords": ["サンプル", "商品", "例"]
}

class ProductStore:
    """商品を管理し、商品が追加されたらリスナーに通知するストア。

    最初のリスナーが登録されたときに、商品を自動で追加するタイマーを開始する。

    Attributes
    ----------
    started : bool
        商品を追加するタイマーを開始済みかどうか。
    listeners : dict[str, list[Callable[[dict[str, Any]], Any]]]
        メッセージ名をキー、コールバックのリストを値とする辞書。
    """

    def __init__(self) -> None:
        """ストアを初期化する。"""
        self.started: bool = False
        self.listeners: dict[str, list[Callable[[dict[str, Any]], Any]]] = {}
        # 5秒ごとに商品をキューに追加するタイマーを作る

    def add_product(self) -> None:
        """ストアに商品を追加し、リスナーに通知する。

        ID・名前・価格・キーワードはランダムに作る。
        """
        product = {
            "id": str(random.randint(10000, 99999)),
            "name": f"商品 {random.randint(1, 100)}",
            "price": round(random.uniform(10.0, 100.0), 2),
            "keywords": [f"キーワード{random.randint(1, 5)}" for _ in range(random.randint(1, 3))]
        }
        self.dispatch_message("new_product", product)

    def start_product_queue_timer(self) -> None:
        """5秒ごとに商品をキューに追加するタイマーを開始する。

        実際には 1〜2 秒後に商品を追加するタイマーを2つ開始する。
        """
        # メインスレッドは stdin の読み取りで止まっているので、商品の追加は別スレッド（threading.Timer）で行う
        def schedule_next() -> None:
            """1〜2 秒後に商品を追加するタイマーを開始する。"""
            delay = random.uniform(1, 2)
            self.product_timer = threading.Timer(delay, self.add_product)
            self.product_timer.start()

        def add_twice() -> None:
            """タイマーを2つ開始する。"""
            schedule_next()
            schedule_next()

        add_twice()

    def add_listener(self, message: str, callback: Callable[[dict[str, Any]], Any]) -> None:
        """商品の更新を受け取るリスナーを追加する。

        最初の呼び出しで、商品を追加するタイマーも開始する。

        Parameters
        ----------
        message : str
            購読するメッセージ名（例: "new_product"）。
        callback : Callable[[dict[str, Any]], Any]
            メッセージを受け取ったときに、ペイロードを引数にして呼ばれる関数。
        """
        if not self.started:
            self.started = True
            self.start_product_queue_timer()
        """商品の更新を受け取るリスナーを追加する。"""
        # 実際のアプリケーションでは、新しい商品が追加されたときに呼ばれるコールバックとして登録する
        callbacks = self.listeners.get(message, [])
        callbacks.append(callback)
        self.listeners[message] = callbacks

    def dispatch_message(self, message: str, payload: dict[str, Any]) -> None:
        """登録されているすべてのリスナーにメッセージを送る。

        Parameters
        ----------
        message : str
            送るメッセージ名。
        payload : dict[str, Any]
            リスナーに渡すデータ。
        """
        callbacks = self.listeners.get(message, [])
        for callback in callbacks:
            callback(payload)

def create_sampling_message(product: dict[str, Any]) -> dict[str, Any]:
    """商品説明の生成を依頼するサンプリングのリクエストを作る。

    Parameters
    ----------
    product : dict[str, Any]
        説明を生成したい商品（id、name、price、keywords を持つ辞書）。

    Returns
    -------
    dict[str, Any]
        sampling/createMessage の JSON-RPC リクエスト。
    """
    # サンプリングは「サーバー → クライアント」へのリクエスト。tools/list などとは向きが逆になる
    # 本来はリクエストごとに一意な id を振り、クライアントからの応答の id と突き合わせる
    sampling_message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "sampling/createMessage",
        "params": {
            # 本来の MCP では、messages の role は user / assistant のみ。システムへの指示は systemPrompt に書く
            "messages": [{
                "role": "system",
                "content": {
                    "type": "text",
                    "text": f"新しい商品が入荷しました: {product['name']}（ID: {product['id']}、価格: {product['price']}）。キーワード: {', '.join(product['keywords'])}"
                }
            }],
            "systemPrompt": "あなたは商品説明の作成を手伝う、親切なアシスタントです",
            # LLM に渡すコンテキストの範囲（none / thisServer / allServers）
            "includeContext": "thisServer",
            "maxTokens": 300
        }
    }
    return sampling_message

def send_sampling_request(product: dict[str, Any]) -> None:
    """商品説明の生成を依頼するサンプリングのリクエストを、クライアントに送る。

    Parameters
    ----------
    product : dict[str, Any]
        説明を生成したい商品（id、name、price、keywords を持つ辞書）。
    """
    print(json.dumps(create_sampling_message(product)))
    # タイマーのスレッドから送るので、flush しないとメインループの次の flush まで送られない
    sys.stdout.flush()

# 新しい商品が追加されたら、その商品説明の生成をクライアントに依頼する
store: ProductStore = ProductStore()
store.add_listener("new_product", send_sampling_request)

def handle_sampling_response(response: dict[str, Any]) -> None:
    """クライアントから届いたサンプリングの応答を処理する。

    Parameters
    ----------
    response : dict[str, Any]
        result.content.text に LLM の生成結果を持つ JSON-RPC 応答。
    """
    content = response['result']['content']['text']
    print("[SERVER] [サンプリングの応答を受信しました]:", content)
    sys.stdout.flush()
    # TODO: 応答を使ってストアを更新するなど、必要な処理を行う

# stdio トランスポートでは「1行 = 1メッセージ」。stdin を1行ずつ読んで処理する。
# 各 case の break で for を抜けても、外側の while True で再び stdin を読み始めるので処理は続く
while True:
    for line in sys.stdin:
        message: str = line.strip()
        if message == "hello":
            print("こんにちは")
            # stdout がパイプだとバッファリングされるので、flush しないとクライアントの readline() が待ち続ける
            sys.stdout.flush()
        # クライアントは json.dumps で送るので、JSON-RPC のメッセージは必ず '{"jsonrpc":' で始まる
        elif message.startswith('{"jsonrpc":'):
            json_message: dict[str, Any] = json.loads(message)
            method: str = json_message.get('method', '')

            # ハンドシェイクが終わるまでは、initialize と notifications/initialized 以外を受け付けない
            if not initialized:
                if method != "initialize" and method != "notifications/initialized":
                    print(f"サーバーが初期化されていません。先に 'initialized' 通知を送ってください。送られたメソッド: {method}")
                    sys.stdout.flush()
                    continue



            match method:
                case "notifications/initialized":
                    # 通知（id を持たないメッセージ）なので、応答は返さない
                    # print("サーバーの初期化に成功しました。")
                    sys.stdout.flush()
                    initialized = True
                    break
                case "initialize":
                    # サーバーの capabilities を返す。ここではまだ initialized にせず、クライアントからの initialized 通知を待つ
                    print(json.dumps(initializeResponse))
                    sys.stdout.flush()
                    # initialized = True
                    break
                     # capabilities を返すべき
                case "tools/call":
                    tool_name: str = json_message['params']['name']
                    args: dict[str, Any] = json_message['params']['args']

                    # tool の処理の途中で、クライアント側の LLM に商品説明の生成を依頼する
                    print(json.dumps(create_sampling_message(product)))
                    sys.stdout.flush()

                    print(json.dumps(progress_notification))
                    sys.stdout.flush()

                    print(json.dumps(progress_notification))
                    sys.stdout.flush()

                    # TODO: tool 呼び出しへの応答を作る（つまり、正しい tool を呼び出す）
                    # 本来の MCP では、引数のキーは "arguments"、結果は {"content": [...]} の形。ここでは独自の形に簡略化している
                    response: dict[str, Any] = {
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
                    # クライアントからのサンプリングの応答は method を持たないので、ここに来る。result の有無で判定する
                    # print(f"不明なメソッドです: {method}")
                    # sys.stdout.flush()
                    if json_message.get('result'):
                        handle_sampling_response(json_message)
                    # サンプリングの応答なので処理する（つまり、ストアを更新する）
                    else:
                        print(f"不明なメソッドです: {json_message['method']}")
                        sys.stdout.flush()
                    break
        # "exit" はこのサンプル独自の終了コマンド（MCP の仕様にはない）。実際の stdio サーバーは stdin が閉じられたら終了する
        elif message == "exit":
            print("サーバーを終了します。")
            sys.stdout.flush()
            sys.exit(0)
        else:
            print(f"不明なメッセージです: {message}")
