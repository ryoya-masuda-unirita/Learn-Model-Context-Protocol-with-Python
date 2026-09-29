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
mcp run server.py
```

## -4- サンプルのテスト

1つのターミナルでサーバーを動かしたまま、別のターミナルを開いて次のコマンドを実行します：

```bash
mcp dev server.py
```

サンプルを画面上でテストできる Web サーバーが起動します。

サーバーに接続できたら：

- tool の一覧を表示して `add` を引数 2 と 4 で実行してみてください。結果に 6 と表示されます。
- resources と resource template を開いて get_greeting を呼び出し、名前を入力してください。入力した名前入りの挨拶が表示されます。

### CLI モードでのテスト

実行した Inspector は実は Node.js のアプリで、`mcp dev` はそのラッパーです。

次のコマンドで、Inspector を直接 CLI モードで起動できます：

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/list
```

サーバーで使えるすべての tool が一覧表示されます。次のような出力になります：

```text
{
  "tools": [
    {
      "name": "get_orders",
      "description": "すべての注文を取得する",
      "inputSchema": {
        "type": "object",
        "properties": {
          "customer_id": {
            "default": 0,
            "title": "Customer Id",
            "type": "integer"
          }
        },
        "title": "get_ordersArguments"
      },
      "outputSchema": {
        "type": "object",
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
        "$defs": {
          "Order": {
            "properties": {
              "id": {
                "format": "uuid",
                "title": "Id",
                "type": "string"
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
        "title": "get_ordersOutput"
      }
    },
    {
      "name": "get_order",
      "description": "ID で注文を取得する",
      "inputSchema": {
        "type": "object",
        "properties": {
          "order_id": {
            "title": "Order Id",
            "type": "integer"
          }
        },
        "required": [
          "order_id"
        ],
        "title": "get_orderArguments"
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "id": {
            "format": "uuid",
            "title": "Id",
            "type": "string"
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
        "title": "Order"
      }
    },
    {
      "name": "place_order",
      "description": "注文する",
      "inputSchema": {
        "type": "object",
        "properties": {
          "customer_id": {
            "title": "Customer Id",
            "type": "integer"
          }
        },
        "required": [
          "customer_id"
        ],
        "title": "place_orderArguments"
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "id": {
            "format": "uuid",
            "title": "Id",
            "type": "string"
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
        "title": "Order"
      }
    },
    {
      "name": "get_cart",
      "description": "カートを1つ取得する",
      "inputSchema": {
        "type": "object",
        "properties": {
          "customer_id": {
            "title": "Customer Id",
            "type": "integer"
          }
        },
        "required": [
          "customer_id"
        ],
        "title": "get_cartArguments"
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "result": {
            "items": {
              "$ref": "#/$defs/Cart"
            },
            "title": "Result",
            "type": "array"
          }
        },
        "required": [
          "result"
        ],
        "$defs": {
          "Cart": {
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
        "title": "get_cartOutput"
      }
    },
    {
      "name": "get_cart_items",
      "description": "カートの中身を取得する",
      "inputSchema": {
        "type": "object",
        "properties": {
          "cart_id": {
            "title": "Cart Id",
            "type": "integer"
          }
        },
        "required": [
          "cart_id"
        ],
        "title": "get_cart_itemsArguments"
      },
      "outputSchema": {
        "type": "object",
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
        "$defs": {
          "CartItem": {
            "properties": {
              "id": {
                "title": "Id",
                "type": "integer"
              },
              "cart_id": {
                "format": "uuid",
                "title": "Cart Id",
                "type": "string"
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
        "title": "get_cart_itemsOutput"
      }
    },
    {
      "name": "add_to_cart",
      "description": "カートに追加する",
      "inputSchema": {
        "type": "object",
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
        "title": "add_to_cartArguments"
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "id": {
            "title": "Id",
            "type": "integer"
          },
          "cart_id": {
            "format": "uuid",
            "title": "Cart Id",
            "type": "string"
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
        "title": "CartItem"
      }
    },
    {
      "name": "get_all_products",
      "description": "すべての商品を取得する",
      "inputSchema": {
        "type": "object",
        "properties": {},
        "title": "get_all_productsArguments"
      },
      "outputSchema": {
        "type": "object",
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
        "$defs": {
          "Product": {
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
        "title": "get_all_productsOutput"
      }
    },
    {
      "name": "get_product",
      "description": "ID で商品を取得する",
      "inputSchema": {
        "type": "object",
        "properties": {
          "product_id": {
            "title": "Product Id",
            "type": "integer"
          }
        },
        "required": [
          "product_id"
        ],
        "title": "get_productArguments"
      },
      "outputSchema": {
        "type": "object",
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
        "title": "Product"
      }
    },
    {
      "name": "get_all_categories",
      "description": "すべてのカテゴリーを取得する",
      "inputSchema": {
        "type": "object",
        "properties": {},
        "title": "get_all_categoriesArguments"
      },
      "outputSchema": {
        "type": "object",
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
        "$defs": {
          "Category": {
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
        "title": "get_all_categoriesOutput"
      }
    },
    {
      "name": "get_all_customers",
      "description": "すべての顧客を取得する",
      "inputSchema": {
        "type": "object",
        "properties": {},
        "title": "get_all_customersArguments"
      },
      "outputSchema": {
        "type": "object",
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
        "$defs": {
          "Customer": {
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
        "title": "get_all_customersOutput"
      }
    }
  ]
}
```

tool を呼び出すには次のように入力します：

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/call --tool-name get_all_categories
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
