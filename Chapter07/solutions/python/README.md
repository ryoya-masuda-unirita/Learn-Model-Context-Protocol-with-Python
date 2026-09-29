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
python client.py
```

次のような出力になります：

```text
LISTING TOOLS
Tool:  add_product_to_cart
Tool:  list_cart
Tool:  get_products
Enter command (or 'quit' to exit):
```

## -4- サンプルのテスト

次の入力でサンプルをテストします。この時点でアプリが起動している前提です。

1. コマンド **get_products** を入力します。次のような出力になります：

  ```text
  Using tool: get_products
  Tool arguments: {'properties': {}, 'title': 'get_productsArguments', 'type': 'object'}
  [05/22/25 15:17:53] INFO     Processing request of type CallToolRequest                                        server.py:551
  Result:  [TextContent(type='text', text='{\n  "type": "text",\n  "name": "Name: Product 1"\n}', annotations=None), TextContent(type='text', text='{\n  "type": "text",\n  "name": "Name: Product 2"\n}', annotations=None), TextContent(type='text', text='{\n  "type": "text",\n  "name": "Name: Product 3"\n}', annotations=None)]
  ```

  選べる商品の一覧があることが分かります。

1. **add_product_to_cart** と入力して、カートに商品を追加します。"Enter product name"（商品名の入力）を求められるので、**Product 2** と入力します。次のような応答が返ってきます：

  ```text
  [05/22/25 15:19:51] INFO     Processing request of type CallToolRequest                                        server.py:551
  Result:  [TextContent(type='text', text='{\n  "type": "text",\n  "name": "ID: 45eef588-3a29-4798-b1ae-44dbfa92075d,product: 2,quantity: 1"\n}', annotations=None)]
  ```

 1. コマンド **list_cart** でカートの中身を一覧表示します。次のような応答が返ってきます：

  ```text
  Using tool: list_cart
  Tool arguments: {'properties': {}, 'title': 'list_cartArguments', 'type': 'object'}
  [05/22/25 15:20:51] INFO     Processing request of type CallToolRequest                                        server.py:551
  Result:  [TextContent(type='text', text='{\n  "type": "text",\n  "name": "ID: 45eef588-3a29-4798-b1ae-44dbfa92075d,product: 2,quantity: 1"\n}', annotations=None)]
  ``` 

  今追加した商品が正しく表示されています。

## LLM サンプルのテスト

1. 依存関係をインストールします（LLM を呼び出せるようにするため）

  ```sh
  pip install openai
  ```

1. 次のように入力して、LLM クライアントを実行します：

  ```sh
  python client_llm.py
  ```

  次のような出力になります：

  ```text
  LISTING TOOLS
  Tool:  add_product_to_cart
  Tool:  list_cart
  Tool:  get_products
  Waiting for input... (type 'quit' to exit)
  Enter prompt:
  ```

1. 次のように **show me products** と入力します：

  ```text
  Enter prompt: show me products
  ```

  次のような出力になります：

  ```text
  ALLING LLM
  TOOL NAME:  get_products
  [05/22/25 16:35:14] INFO     Processing request of type CallToolRequest                                        server.py:551
  TOOLS result:  [TextContent(type='text', text='{\n  "type": "text",\n  "name": "Name: Product 1"\n}', annotations=None), TextContent(type='text', text='{\n  "type": "text",\n  "name": "Name: Product 2"\n}', annotations=None), TextContent(type='text', text='{\n  "type": "text",\n  "name": "Name: Product 3"\n}', annotations=None)]
  Waiting for input... (type 'quit' to exit)
  ```

1. 次に **Add Product 1 to the cart** と入力して商品を追加します。次のような出力になります：

  ```text
  CALLING LLM
  TOOL NAME:  add_product_to_cart
  [05/22/25 17:21:31] INFO     Processing request of type CallToolRequest                                        server.py:551
  TOOLS result:  [TextContent(type='text', text='{\n  "type": "text",\n  "name": "ID: 921f95e8-0855-40ca-8587-8a6e38bfd69d,product: 1,quantity: 1"\n}', annotations=None)]
  Waiting for input... (type 'quit' to exit)
  ```

1. **show me cart content** と入力して確認してみましょう。次のような出力になります：

  ```text
  CALLING LLM
  TOOL NAME:  list_cart
  [05/22/25 17:23:10] INFO     Processing request of type CallToolRequest                                        server.py:551
  TOOLS result:  [TextContent(type='text', text='{\n  "type": "text",\n  "name": "ID: 9d0e23f3-23d5-4d7e-bfa9-71be86b26f04,product: 1,quantity: 1"\n}', annotations=None)]
  Waiting for input... (type 'quit' to exit)
  ````

  追加した商品がカートに入っていることが分かります。
