# このサンプルの実行

`uv` のインストールを推奨しますが、必須ではありません。[手順](https://docs.astral.sh/uv/#highlights)を参照してください。

## -0- 仮想環境の作成

```bash
python -m venv venv
```

## -1- 仮想環境の有効化

```bash
venv\Scrips\activate
```

## -2- 依存関係のインストール

```bash
pip install "mcp[cli]"
```

## -3- サンプルの実行


```bash
uvicorn server:app --port 3000
```

## -4- サンプルのテスト

1つのターミナルでサーバーを動かしたまま、別のターミナルを開いて次のコマンドを実行します：

```bash
curl http://127.0.0.1:3000/sse
```

次のような応答が返ってきます：

```text
event: endpoint
data: /messages/?session_id=262edd9eb4ba4185abe28756eba2c7f1
```

つまり、`session_id` が表示されれば OK です。SSE サーバーが応答し、ハンドシェイクを行っていることを意味します。

### CLI モードでのテスト

Inspector は実は Node.js のアプリで、`mcp dev` はそのラッパーです。

次のコマンドで、Inspector を直接 CLI モードで起動できます：

```bash
npx @modelcontextprotocol/inspector --cli http://localhost:3000/sse --method tools/list
```

サーバーで使えるすべての tool が一覧表示されます。次のような出力になります：

```text
{
  "tools": [
    {
      "name": "get_products_by_category",
      "description": "カテゴリーで商品を取得する。\n\nParameters\n----------\ncategory : str\n    取得する商品のカテゴリー名（例: \"カテゴリー 1\"）。\n\nReturns\n-------\nList[Product]\n    指定したカテゴリーの商品のリスト。\n",
      "inputSchema": {
        "properties": {
          "category": {
            "title": "Category",
            "type": "string"
          }
        },
        "required": [
          "category"
        ],
        "title": "get_products_by_categoryArguments",
        "type": "object"
      },
      "outputSchema": {
        "$defs": {
          "Product": {
            "description": "商品。",
            "properties": {
              "id": {
                "title": "Id",
                "type": "integer"
              },
              "name": {
                "title": "Name",
                "type": "string"
              },
              "price": {
                "title": "Price",
                "type": "number"
              },
              "description": {
                "title": "Description",
                "type": "string"
              },
              "category": {
                "title": "Category",
                "type": "string"
              }
            },
            "required": [
              "id",
              "name",
              "price",
              "description",
              "category"
            ],
            "title": "Product",
            "type": "object"
          }
        },
        "properties": {
          "result": {
            "items": {
              "$ref": "#/$defs/Product"
            },
            "title": "Result",
            "type": "array"
          }
        },
        "required": [
          "result"
        ],
        "title": "get_products_by_categoryOutput",
        "type": "object"
      }
    },
    {
      "name": "add_product_to_cart",
      "description": "カートに商品を追加する。\n\nParameters\n----------\nproduct_name : str\n    追加する商品の名前（例: \"商品 1\"）。\n\nReturns\n-------\nCartItem\n    追加したカートの商品。\n\nRaises\n------\nValueError\n    指定した名前の商品が見つからない場合。\n",
      "inputSchema": {
        "properties": {
          "product_name": {
            "title": "Product Name",
            "type": "string"
          }
        },
        "required": [
          "product_name"
        ],
        "title": "add_product_to_cartArguments",
        "type": "object"
      },
      "outputSchema": {
        "description": "カートに入っている商品。",
        "properties": {
          "cart_id": {
            "title": "Cart Id",
            "type": "integer"
          },
          "product_id": {
            "title": "Product Id",
            "type": "integer"
          },
          "quantity": {
            "title": "Quantity",
            "type": "integer"
          }
        },
        "required": [
          "cart_id",
          "product_id",
          "quantity"
        ],
        "title": "CartItem",
        "type": "object"
      }
    },
    {
      "name": "list_cart",
      "description": "カートの中身をすべて一覧表示する。\n\nReturns\n-------\nList[CartItem]\n    カートに入っている商品のリスト。\n",
      "inputSchema": {
        "properties": {},
        "title": "list_cartArguments",
        "type": "object"
      },
      "outputSchema": {
        "$defs": {
          "CartItem": {
            "description": "カートに入っている商品。",
            "properties": {
              "cart_id": {
                "title": "Cart Id",
                "type": "integer"
              },
              "product_id": {
                "title": "Product Id",
                "type": "integer"
              },
              "quantity": {
                "title": "Quantity",
                "type": "integer"
              }
            },
            "required": [
              "cart_id",
              "product_id",
              "quantity"
            ],
            "title": "CartItem",
            "type": "object"
          }
        },
        "properties": {
          "result": {
            "items": {
              "$ref": "#/$defs/CartItem"
            },
            "title": "Result",
            "type": "array"
          }
        },
        "required": [
          "result"
        ],
        "title": "list_cartOutput",
        "type": "object"
      }
    },
    {
      "name": "get_products",
      "description": "すべての商品を取得する。\n\nReturns\n-------\nList[Product]\n    すべての商品のリスト。\n",
      "inputSchema": {
        "properties": {},
        "title": "get_productsArguments",
        "type": "object"
      },
      "outputSchema": {
        "$defs": {
          "Product": {
            "description": "商品。",
            "properties": {
              "id": {
                "title": "Id",
                "type": "integer"
              },
              "name": {
                "title": "Name",
                "type": "string"
              },
              "price": {
                "title": "Price",
                "type": "number"
              },
              "description": {
                "title": "Description",
                "type": "string"
              },
              "category": {
                "title": "Category",
                "type": "string"
              }
            },
            "required": [
              "id",
              "name",
              "price",
              "description",
              "category"
            ],
            "title": "Product",
            "type": "object"
          }
        },
        "properties": {
          "result": {
            "items": {
              "$ref": "#/$defs/Product"
            },
            "title": "Result",
            "type": "array"
          }
        },
        "required": [
          "result"
        ],
        "title": "get_productsOutput",
        "type": "object"
      }
    }
  ]
}
```

tool を呼び出すには次のように入力します：

```bash
npx @modelcontextprotocol/inspector --cli http://127.0.0.1:3000/sse --method tools/call --tool-name list_cart
```

次のような出力になります：

```text
{
  "content": [],
  "structuredContent": {
    "result": []
  },
  "isError": false
}
```

まだカートに商品を追加していないので、これは想定どおりの結果です。

カートに商品を追加するには、次のコマンドを実行します：

```bash
npx @modelcontextprotocol/inspector --cli http://127.0.0.1:3000/sse --method tools/call --tool-name add_product_to_cart --tool-arg product_name="商品 1"
```

次のような出力になります：

```text
{
  "content": [
    {
      "type": "text",
      "text": "{\n  \"cart_id\": 1,\n  \"product_id\": 1,\n  \"quantity\": 1\n}"       
    }
  ],
  "structuredContent": {
    "cart_id": 1,
    "product_id": 1,
    "quantity": 1
  },
  "isError": false
}
```

これは、今カートに追加した商品の ID を含むサーバーからの応答です。次のコマンドで、もう一度カートの中身を一覧表示できます：

```bash
npx @modelcontextprotocol/inspector --cli http://127.0.0.1:3000/sse --method tools/call --tool-name list_cart
```

今度は次のように表示されます：

```text
{
  "content": [
    {
      "type": "text",
      "text": "{\n  \"cart_id\": 1,\n  \"product_id\": 1,\n  \"quantity\": 1\n}"       
    }
  ],
  "structuredContent": {
    "result": [
      {
        "cart_id": 1,
        "product_id": 1,
        "quantity": 1
      }
    ]
  },
  "isError": false
}
```
