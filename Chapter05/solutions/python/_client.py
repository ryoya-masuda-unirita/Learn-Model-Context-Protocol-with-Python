import requests

import json
port = 8000

def consume_stream():
    headers = {
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

    headers['mcp-session-id'] = response.headers.get('mcp-session-id')

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

    for line in response.iter_lines():
        if line:
            print(line.decode('utf-8'))

    print("tool を呼び出しています: echo...")
    response = requests.post(
        f'http://localhost:{port}/mcp', 
        stream=True, 
        headers=headers,
        data=json.dumps(callTool))

    print("tool 呼び出しのヘッダー:", response.headers)

    for line in response.iter_lines():
        if line:
            print(line.decode('utf-8'))

consume_stream()