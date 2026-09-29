"""クライアントとサーバーでやり取りする JSON-RPC メッセージの定義。

MCP の initialize / initialized / tools/list などのメッセージを、辞書として定義する。
"""
from typing import Any

list_tools_message: dict[str, Any] = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
};

initialize_message: dict[str, Any] = {
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
};

server_name: str = "ExampleServer"
server_version: str = "1.0.0"

initializeResponse: dict[str, Any] = {
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "protocolVersion": "2024-11-05",
        "capabilities": {
        "logging": {},
        "prompts": {
            "listChanged": True
        },
        "resources": {
            "subscribe": True,
            "listChanged": True
        },
        "tools": {
            "listChanged": True
        }
        },
        "serverInfo": {
        "name": server_name,
        "version": server_version
        }
    }
};

initialized_message: dict[str, Any] = {
    "jsonrpc": "2.0",
    "method": "notifications/initialized",
    "params": {}
};