
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

このサンプルは、LLM として Amazon Bedrock の GPT-5.5（モデル ID `openai.gpt-5.5`、リージョン us-east-1）を、OpenAI 互換 API で呼び出します。実行には次のものが必要です：

- Bedrock を使える AWS の認証情報（`aws configure` などで設定したプロファイル）
- Bedrock で OpenAI の GPT-5.5 が使える状態になっていること

Bedrock の API キーは、実行時に AWS の認証情報から短期トークンを自動で作るので、別途発行する必要はありません。使うプロファイルは環境変数 `AWS_PROFILE` で指定します。

1. 次のように入力して、LLM クライアントを実行します（`<プロファイル名>` は自分の AWS のプロファイル名に置き換えます）：

```sh
  AWS_PROFILE=<プロファイル名> uv run python client_llm.py
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

  LLM が get_products tool を選んで呼び出し、次のような出力になります：

```text
  LLM を呼び出しています
  tool 名:  get_products
  tool の結果:  [TextContent(type='text', text='{\n  "id": 1,\n  "name": "商品 1",\n  "price": 10.0,\n  "description": "商品 1 の説明",\n  "category": "カテゴリー 1"\n}', annotations=None, meta=None), TextContent(type='text', text='{\n  "id": 2,\n  "name": "商品 2",\n  "price": 20.0,\n  "description": "商品 2 の説明",\n  "category": "カテゴリー 2"\n}', annotations=None, meta=None), TextContent(type='text', text='{\n  "id": 3,\n  "name": "商品 3",\n  "price": 30.0,\n  "description": "商品 3 の説明",\n  "category": "カテゴリー 3"\n}', annotations=None, meta=None)]
  入力を待っています...（'quit' で終了）
```

1. 次に **商品 1 をカートに追加して** と入力して商品を追加します。次のような出力になります：

```text
  LLM を呼び出しています
  tool 名:  add_product_to_cart
  tool の結果:  [TextContent(type='text', text='{\n  "cart_id": 0,\n  "product_id": 1,\n  "quantity": 1\n}', annotations=None, meta=None)]
  入力を待っています...（'quit' で終了）
```

1. **カートの中身を見せて** と入力して確認してみましょう。次のような出力になります：

```text
  LLM を呼び出しています
  tool 名:  list_cart
  tool の結果:  [TextContent(type='text', text='{\n  "cart_id": 0,\n  "product_id": 1,\n  "quantity": 1\n}', annotations=None, meta=None)]
  入力を待っています...（'quit' で終了）
```

  追加した商品がカートに入っていることが分かります。
