"""クライアントとサーバーでやり取りする JSON-RPC メッセージの定義。

MCP の initialize / initialized / tools/list などのメッセージを、辞書として定義する。
"""
from typing import Any

# id を持つので「リクエスト」。サーバーは同じ id を付けて応答を返す
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
    # クライアントが使いたいプロトコルのバージョン。サーバーは対応できるバージョンを応答で返す
    "protocolVersion": "2024-11-05",
    # クライアントが提供できる機能（roots、sampling）をサーバーに伝える
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

# 本来は initialize リクエストの id をそのまま返す。ここでは簡略化のため 1 に固定している
initializeResponse: dict[str, Any] = {
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "protocolVersion": "2024-11-05",
        # サーバーが提供できる機能。listChanged は、一覧が変わったときに通知を送れることを示す
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

# id を持たないので「通知」。サーバーは応答を返さない
initialized_message: dict[str, Any] = {
    "jsonrpc": "2.0",
    "method": "notifications/initialized",
    "params": {}
};