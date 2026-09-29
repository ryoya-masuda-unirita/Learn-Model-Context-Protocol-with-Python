"""MCP サーバー（server.py）の /mcp に initialize を POST し、返ってきたストリームを表示するテスト用クライアント。"""
from typing import Any

import requests
import json

message: dict[str, Any] = {
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

headers: dict[str, str] = {
        'Accept': 'application/json, text/event-stream',
        'Content-Type': 'application/json'
    }

response = requests.post(
        f'http://localhost:{8000}/mcp', 
        stream=True, 
        headers=headers,
        data=json.dumps(message))

for line in response.iter_lines():
        if line:
            print(line.decode('utf-8'))