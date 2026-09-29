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
uv run python client.py
```

次のような出力になります：

```text
tool の一覧
tool:  add_product_to_cart
tool:  list_cart
tool:  get_products
コマンドを入力してください（'quit' で終了）:
```

## -2- サンプルのテスト

次の入力でサンプルをテストします。この時点でアプリが起動している前提です。

1. コマンド **get_products** を入力します。次のような出力になります：

  ```text
  使用する tool: get_products
  tool の引数: {'properties': {}, 'title': 'get_productsArguments', 'type': 'object'}
  [05/22/25 15:17:53] INFO     Processing request of type CallToolRequest                                        server.py:551
  結果:  [TextContent(type='text', text='{\n  "type": "text",\n  "name": "Name: 商品 1"\n}', annotations=None), TextContent(type='text', text='{\n  "type": "text",\n  "name": "Name: 商品 2"\n}', annotations=None), TextContent(type='text', text='{\n  "type": "text",\n  "name": "Name: 商品 3"\n}', annotations=None)]
  ```

  選べる商品の一覧があることが分かります。

1. **add_product_to_cart** と入力して、カートに商品を追加します。"product_name を入力してください" と求められるので、**商品 2** と入力します。次のような応答が返ってきます：

  ```text
  [05/22/25 15:19:51] INFO     Processing request of type CallToolRequest                                        server.py:551
  結果:  [TextContent(type='text', text='{\n  "type": "text",\n  "name": "ID: 45eef588-3a29-4798-b1ae-44dbfa92075d,product: 2,quantity: 1"\n}', annotations=None)]
  ```

 1. コマンド **list_cart** でカートの中身を一覧表示します。次のような応答が返ってきます：

  ```text
  使用する tool: list_cart
  tool の引数: {'properties': {}, 'title': 'list_cartArguments', 'type': 'object'}
  [05/22/25 15:20:51] INFO     Processing request of type CallToolRequest                                        server.py:551
  結果:  [TextContent(type='text', text='{\n  "type": "text",\n  "name": "ID: 45eef588-3a29-4798-b1ae-44dbfa92075d,product: 2,quantity: 1"\n}', annotations=None)]
  ``` 

  今追加した商品が正しく表示されています。

## LLM サンプルのテスト

1. 次のように入力して、LLM クライアントを実行します：

  ```sh
  uv run python client_llm.py
  ```

  次のような出力になります：

  ```text
  tool の一覧
  tool:  add_product_to_cart
  tool:  list_cart
  tool:  get_products
  入力を待っています...（'quit' で終了）
  プロンプトを入力してください:
  ```

1. 次のように **商品を見せて** と入力します：

  ```text
  プロンプトを入力してください: 商品を見せて
  ```

  次のような出力になります：

  ```text
  LLM を呼び出しています
  tool 名:  get_products
  [05/22/25 16:35:14] INFO     Processing request of type CallToolRequest                                        server.py:551
  tool の結果:  [TextContent(type='text', text='{\n  "type": "text",\n  "name": "Name: 商品 1"\n}', annotations=None), TextContent(type='text', text='{\n  "type": "text",\n  "name": "Name: 商品 2"\n}', annotations=None), TextContent(type='text', text='{\n  "type": "text",\n  "name": "Name: 商品 3"\n}', annotations=None)]
  入力を待っています...（'quit' で終了）
  ```

1. 次に **商品 1 をカートに追加して** と入力して商品を追加します。次のような出力になります：

  ```text
  LLM を呼び出しています
  tool 名:  add_product_to_cart
  [05/22/25 17:21:31] INFO     Processing request of type CallToolRequest                                        server.py:551
  tool の結果:  [TextContent(type='text', text='{\n  "type": "text",\n  "name": "ID: 921f95e8-0855-40ca-8587-8a6e38bfd69d,product: 1,quantity: 1"\n}', annotations=None)]
  入力を待っています...（'quit' で終了）
  ```

1. **カートの中身を見せて** と入力して確認してみましょう。次のような出力になります：

  ```text
  LLM を呼び出しています
  tool 名:  list_cart
  [05/22/25 17:23:10] INFO     Processing request of type CallToolRequest                                        server.py:551
  tool の結果:  [TextContent(type='text', text='{\n  "type": "text",\n  "name": "ID: 9d0e23f3-23d5-4d7e-bfa9-71be86b26f04,product: 1,quantity: 1"\n}', annotations=None)]
  入力を待っています...（'quit' で終了）
  ````

  追加した商品がカートに入っていることが分かります。
