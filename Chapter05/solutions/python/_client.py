"""SDK を使わず、requests で Streamable HTTP の MCP サーバーとやり取りするクライアント。"""
import requests

import json
port: int = 8000

def consume_stream() -> None:
    """initialize、initialized、tools/list、tools/call を順に POST し、応答を表示する。

    最初の応答ヘッダーで受け取った mcp-session-id を、以降のリクエストに付ける。
    """
    # Streamable HTTP では、クライアントは JSON と SSE の両方を受け取れると宣言しなければならない。
    # サーバーは応答の内容に応じて、どちらの形式で返すかを決める
    headers: dict[str, str] = {
        'Accept': 'application/json, text/event-stream',
        'Content-Type': 'application/json'
    }

    # initialized を含む JSON-RPC メッセージ
    message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
            "roots": {
                "listChanged": True
            },
            "sampling": {}
            },
            "clientInfo": {
            "name": "ExampleClient",
            "version": "1.0.0"
            }
        }
    }

    initialized = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }

    listTools = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }

    callTool = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "echo",
            # 本来の MCP の引数のキーは "arguments"（Chapter02 の独自実装では "args" に簡略化していた）
            "arguments": {
                "message": "chris"
            }
        }
    }

    # /mcp に POST すると session_id が得られる
    # GET でセッションが返ってくるはず
    # データはどこに POST する？

    response = requests.post(
        f'http://localhost:{port}/mcp', 
        stream=True, 
        headers=headers,
        data=json.dumps(message))
    
    print("セッション ID:", response.headers.get('mcp-session-id'))
    
    # for line in response.iter_lines():
    #     if line:
    #         print(line.decode('utf-8'))

    # print("ヘッダー: ",response.headers)
    # session_id = response.headers.get('mcp-session-id')
    # print("セッション ID:", session_id)

    # サーバーは initialize の応答の Mcp-Session-Id ヘッダーでセッション ID を割り当てる。
    # 以降のリクエストにこの ID を付けないと、サーバーはどのセッションのリクエストかわからず 400 エラーを返す
    session_id = response.headers.get('mcp-session-id')
    if session_id is None:
        raise RuntimeError("サーバーからセッション ID（mcp-session-id ヘッダー）が返ってきませんでした")
    headers['mcp-session-id'] = session_id

    # 通知（id なし）には応答がない。サーバーは本文なしの 202 Accepted を返す
    print("initialized を送信しています...")
    response = requests.post(
        f'http://localhost:{port}/mcp', 
        stream=True, 
        headers=headers,
        data=json.dumps(initialized))

    print("tool の一覧を取得しています...")
    response = requests.post(
        f'http://localhost:{port}/mcp', 
        stream=True, 
        headers=headers,
        data=json.dumps(listTools))

    # 応答は SSE の形式（event: message の行と data: の行）で届く
    for line in response.iter_lines():
        if line:
            print(line.decode('utf-8'))

    print("tool を呼び出しています: echo...")
    response = requests.post(
        f'http://localhost:{port}/mcp', 
        stream=True, 
        headers=headers,
        data=json.dumps(callTool))

    # tool の途中で送られるログの通知も、最後の結果と同じ SSE のストリームに順に流れてくる
    print("tool 呼び出しのヘッダー:", response.headers)

    for line in response.iter_lines():
        if line:
            print(line.decode('utf-8'))

consume_stream()