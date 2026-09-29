# このサンプルの実行

`uv` を使います。インストール方法は[手順](https://docs.astral.sh/uv/#highlights)を参照してください。

## -0- 環境のセットアップ

[uv](https://docs.astral.sh/uv/) で依存関係をインストールします（初回のみ）。リポジトリ内のどのディレクトリで実行しても、リポジトリ直下の `.venv` にインストールされます：

```bash
uv sync
```

以降のコマンドは `uv run` を付けて実行します。仮想環境を有効化する必要はありません。

## -1- サンプルの実行


```bash
uv run mcp run server.py
```

## -2- サンプルのテスト

1つのターミナルでサーバーを動かしたまま、別のターミナルを開いて次のコマンドを実行します：

```bash
uv run mcp dev server.py
```

サンプルを画面上でテストできる Web サーバーが起動します。

サーバーに接続できたら：

- tool の一覧を表示して `add` を引数 2 と 4 で実行してみてください。結果に 6 と表示されます。
- resources と resource template を開いて get_greeting を呼び出し、名前を入力してください。入力した名前入りの挨拶が表示されます。

### CLI モードでのテスト

実行した Inspector は実は Node.js のアプリで、`mcp dev` はそのラッパーです。

次のコマンドで、Inspector を直接 CLI モードで起動できます：

```bash
npx @modelcontextprotocol/inspector --cli uv run mcp run server.py --method tools/list
```

サーバーで使えるすべての tool が一覧表示されます。次のような出力になります：

```text
{
  "tools": [
    {
      "name": "get_orders",
      "description": "すべての注文を取得する。\n\nParameters\n----------\ncustomer_id : int, optional\n    絞り込む顧客の ID。0 ならすべての注文を返す。デフォルトは 0。\n\nReturns\n-------\nList[Order]\n    条件に合う注文のリスト。\n\nRaises\n------\nValueError\n    存在しない顧客の ID が指定された場合。\n",
      "inputSchema": {
        "properties": {
          "customer_id": {
            "default": 0,
            "title": "Customer Id",
            "type": "integer"
          }
        },
        "title": "get_ordersArguments",
        "type": "object"
      },
      "outputSchema": {
        "$defs": {
          "Order": {
            "description": "注文。",
            "properties": {
              "id": {
                "title": "Id",
                "type": "integer"
              },
              "customer_id": {
                "title": "Customer Id",
                "type": "integer"
              }
            },
            "required": [
              "id",
              "customer_id"
            ],
            "title": "Order",
            "type": "object"
          }
        },
        "properties": {
          "result": {
            "items": {
              "$ref": "#/$defs/Order"
            },
            "title": "Result",
            "type": "array"
          }
        },
        "required": [
          "result"
        ],
        "title": "get_ordersOutput",
        "type": "object"
      }
    },
    {
      "name": "get_order",
      "description": "ID で注文を取得する。\n\nParameters\n----------\norder_id : int\n    取得する注文の ID。\n\nReturns\n-------\nOrder | None\n    見つかった注文。見つからなければ None。\n",
      "inputSchema": {
        "properties": {
          "order_id": {
            "title": "Order Id",
            "type": "integer"
          }
        },
        "required": [
          "order_id"
        ],
        "title": "get_orderArguments",
        "type": "object"
      },
      "outputSchema": {
        "$defs": {
          "Order": {
            "description": "注文。",
            "properties": {
              "id": {
                "title": "Id",
                "type": "integer"
              },
              "customer_id": {
                "title": "Customer Id",
                "type": "integer"
              }
            },
            "required": [
              "id",
              "customer_id"
            ],
            "title": "Order",
            "type": "object"
          }
        },
        "properties": {
          "result": {
            "anyOf": [
              {
                "$ref": "#/$defs/Order"
              },
              {
                "type": "null"
              }
            ]
          }
        },
        "required": [
          "result"
        ],
        "title": "get_orderOutput",
        "type": "object"
      }
    },
    {
      "name": "place_order",
      "description": "注文する。\n\nParameters\n----------\ncustomer_id : int\n    注文する顧客の ID。\n\nReturns\n-------\nOrder\n    作成した注文。\n\nRaises\n------\nValueError\n    存在しない顧客の ID が指定された場合。\n",
      "inputSchema": {
        "properties": {
          "customer_id": {
            "title": "Customer Id",
            "type": "integer"
          }
        },
        "required": [
          "customer_id"
        ],
        "title": "place_orderArguments",
        "type": "object"
      },
      "outputSchema": {
        "description": "注文。",
        "properties": {
          "id": {
            "title": "Id",
            "type": "integer"
          },
          "customer_id": {
            "title": "Customer Id",
            "type": "integer"
          }
        },
        "required": [
          "id",
          "customer_id"
        ],
        "title": "Order",
        "type": "object"
      }
    },
    {
      "name": "get_cart",
      "description": "カートを1つ取得する。\n\nParameters\n----------\ncustomer_id : int\n    カートを持つ顧客の ID。\n\nReturns\n-------\nCart | None\n    見つかったカート。見つからなければ None。\n\nRaises\n------\nValueError\n    存在しない顧客の ID が指定された場合。\n",
      "inputSchema": {
        "properties": {
          "customer_id": {
            "title": "Customer Id",
            "type": "integer"
          }
        },
        "required": [
          "customer_id"
        ],
        "title": "get_cartArguments",
        "type": "object"
      },
      "outputSchema": {
        "$defs": {
          "Cart": {
            "description": "顧客のカート。",
            "properties": {
              "id": {
                "title": "Id",
                "type": "integer"
              },
              "customer_id": {
                "title": "Customer Id",
                "type": "integer"
              }
            },
            "required": [
              "id",
              "customer_id"
            ],
            "title": "Cart",
            "type": "object"
          }
        },
        "properties": {
          "result": {
            "anyOf": [
              {
                "$ref": "#/$defs/Cart"
              },
              {
                "type": "null"
              }
            ]
          }
        },
        "required": [
          "result"
        ],
        "title": "get_cartOutput",
        "type": "object"
      }
    },
    {
      "name": "get_cart_items",
      "description": "カートの中身を取得する。\n\nParameters\n----------\ncart_id : int\n    中身を取得するカートの ID。\n\nReturns\n-------\nList[CartItem]\n    カートに入っている商品のリスト。\n",
      "inputSchema": {
        "properties": {
          "cart_id": {
            "title": "Cart Id",
            "type": "integer"
          }
        },
        "required": [
          "cart_id"
        ],
        "title": "get_cart_itemsArguments",
        "type": "object"
      },
      "outputSchema": {
        "$defs": {
          "CartItem": {
            "description": "カートに入っている商品。",
            "properties": {
              "id": {
                "title": "Id",
                "type": "integer"
              },
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
              "id",
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
        "title": "get_cart_itemsOutput",
        "type": "object"
      }
    },
    {
      "name": "add_to_cart",
      "description": "カートに追加する。\n\nParameters\n----------\ncart_id : int\n    追加先のカートの ID。\nproduct_id : int\n    追加する商品の ID。\nquantity : int\n    数量。\n\nReturns\n-------\nCartItem\n    追加したカートの商品。\n",
      "inputSchema": {
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
        "title": "add_to_cartArguments",
        "type": "object"
      },
      "outputSchema": {
        "description": "カートに入っている商品。",
        "properties": {
          "id": {
            "title": "Id",
            "type": "integer"
          },
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
          "id",
          "cart_id",
          "product_id",
          "quantity"
        ],
        "title": "CartItem",
        "type": "object"
      }
    },
    {
      "name": "get_all_products",
      "description": "すべての商品を取得する。\n\nReturns\n-------\nList[Product]\n    すべての商品のリスト。\n",
      "inputSchema": {
        "properties": {},
        "title": "get_all_productsArguments",
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
              }
            },
            "required": [
              "id",
              "name",
              "price",
              "description"
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
        "title": "get_all_productsOutput",
        "type": "object"
      }
    },
    {
      "name": "get_product",
      "description": "ID で商品を取得する。\n\nParameters\n----------\nproduct_id : int\n    取得する商品の ID。\n\nReturns\n-------\nProduct | None\n    見つかった商品。見つからなければ None。\n",
      "inputSchema": {
        "properties": {
          "product_id": {
            "title": "Product Id",
            "type": "integer"
          }
        },
        "required": [
          "product_id"
        ],
        "title": "get_productArguments",
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
              }
            },
            "required": [
              "id",
              "name",
              "price",
              "description"
            ],
            "title": "Product",
            "type": "object"
          }
        },
        "properties": {
          "result": {
            "anyOf": [
              {
                "$ref": "#/$defs/Product"
              },
              {
                "type": "null"
              }
            ]
          }
        },
        "required": [
          "result"
        ],
        "title": "get_productOutput",
        "type": "object"
      }
    },
    {
      "name": "get_all_categories",
      "description": "すべてのカテゴリーを取得する。\n\nReturns\n-------\nList[Category]\n    すべてのカテゴリーのリスト。\n",
      "inputSchema": {
        "properties": {},
        "title": "get_all_categoriesArguments",
        "type": "object"
      },
      "outputSchema": {
        "$defs": {
          "Category": {
            "description": "商品カテゴリー。",
            "properties": {
              "id": {
                "format": "uuid",
                "title": "Id",
                "type": "string"
              },
              "name": {
                "title": "Name",
                "type": "string"
              },
              "description": {
                "title": "Description",
                "type": "string"
              }
            },
            "required": [
              "id",
              "name",
              "description"
            ],
            "title": "Category",
            "type": "object"
          }
        },
        "properties": {
          "result": {
            "items": {
              "$ref": "#/$defs/Category"
            },
            "title": "Result",
            "type": "array"
          }
        },
        "required": [
          "result"
        ],
        "title": "get_all_categoriesOutput",
        "type": "object"
      }
    },
    {
      "name": "get_all_customers",
      "description": "すべての顧客を取得する。\n\nReturns\n-------\nList[Customer]\n    すべての顧客のリスト。\n",
      "inputSchema": {
        "properties": {},
        "title": "get_all_customersArguments",
        "type": "object"
      },
      "outputSchema": {
        "$defs": {
          "Customer": {
            "description": "顧客。",
            "properties": {
              "id": {
                "title": "Id",
                "type": "integer"
              },
              "name": {
                "title": "Name",
                "type": "string"
              },
              "email": {
                "title": "Email",
                "type": "string"
              }
            },
            "required": [
              "id",
              "name",
              "email"
            ],
            "title": "Customer",
            "type": "object"
          }
        },
        "properties": {
          "result": {
            "items": {
              "$ref": "#/$defs/Customer"
            },
            "title": "Result",
            "type": "array"
          }
        },
        "required": [
          "result"
        ],
        "title": "get_all_customersOutput",
        "type": "object"
      }
    }
  ]
}
```

tool を呼び出すには次のように入力します：

```bash
npx @modelcontextprotocol/inspector --cli uv run mcp run server.py --method tools/call --tool-name get_all_categories
```

次のような出力になります：

```text
{
  "content": [
    {
      "type": "text",
      "text": "{\n  \"id\": \"a231765d-7eae-4462-9042-a6e00b211bf0\",\n  \"name\": \"カテゴリー 1\",\n  \"description\": \"カテゴリー 1 の説明\"\n}"
    },
    {
      "type": "text",
      "text": "{\n  \"id\": \"50285d76-e7b8-4939-b2df-08452750b5da\",\n  \"name\": \"カテゴリー 2\",\n  \"description\": \"カテゴリー 2 の説明\"\n}"
    },
    {
      "type": "text",
      "text": "{\n  \"id\": \"fdd934ee-f8c8-47dc-ab63-1efe68a8bbb2\",\n  \"name\": \"カテゴリー 3\",\n  \"description\": \"カテゴリー 3 の説明\"\n}"
    }
  ],
  "structuredContent": {
    "result": [
      {
        "id": "a231765d-7eae-4462-9042-a6e00b211bf0",
        "name": "カテゴリー 1",
        "description": "カテゴリー 1 の説明"
      },
      {
        "id": "50285d76-e7b8-4939-b2df-08452750b5da",
        "name": "カテゴリー 2",
        "description": "カテゴリー 2 の説明"
      },
      {
        "id": "fdd934ee-f8c8-47dc-ab63-1efe68a8bbb2",
        "name": "カテゴリー 3",
        "description": "カテゴリー 3 の説明"
      }
    ]
  },
  "isError": false
}
```

> ![!TIP]
> 通常、Inspector はブラウザより CLI モードで実行する方がずっと速いです。
> Inspector の詳細は[こちら](https://github.com/modelcontextprotocol/inspector)を参照してください。
