# サンプルの実行

## 環境のセットアップ

```sh
python -m venv venv
source ./venv/bin/activate
```

## 依存関係のインストール

```sh
pip install "mcp[cli]" openai
```

## 実行

```sh
python sample-client.py
```

次のような出力になります：

```text
[08/16/25 19:31:40] INFO     Processing request of type CallToolRequest               server.py:624
サンプリングのリクエスト: [SamplingMessage(role='user', content=TextContent(type='text', text='パプリカ の商品説明を作成してください。特徴: 赤い、みずみずしい、野菜', annotations=None, meta=None))]
[08/16/25 19:31:43] INFO     Processing request of type ListToolsRequest              server.py:624
結果: {"id": 1, "name": "パプリカ", "description": "**Product Description: Paprika \u2013 The Vibrant Touch of Flavor**\n\nElevate your culinary creations with our premium Paprika, a stunning red spice derived from the most luscious, juicy peppers. This vibrant addition is more than just a seasoning; it\u2019s a burst of color and taste that brings warmth and depth to every dish.\n\nOur Paprika is sourced from high-quality, sun-ripened vegetables, meticulously harvested at their peak to ensure maximum flavor. With its rich, sweet notes and subtle smokiness, this natural spice delivers a delightful punch that enhances everything from savory stews and roasted meats to vibrant vegetable dishes and sauces.\n\nNot only is our Paprika a feast for the eyes with its brilliant red hue, but it's also packed with antioxidants and vitamins, making it a nutritious choice for health-conscious cooks. Whether you sprinkle it onto a beloved family recipe or use it to create something intentionally new, our Paprika is versatile enough to brighten any meal.\n\nTransform everyday cooking into an extraordinary experience with the irresistible"}
                    INFO     Processing request of type CallToolRequest               server.py:624

結果: {
  "id": 1,
  "name": "パプリカ",
  "description": "**Product Description: Paprika – The Vibrant Touch of Flavor**\n\nElevate your culinary creations with our premium Paprika, a stunning red spice derived from the most luscious, juicy peppers. This vibrant addition is more than just a seasoning; it’s a burst of color and taste that brings warmth and depth to every dish.\n\nOur Paprika is sourced from high-quality, sun-ripened vegetables, meticulously harvested at their peak to ensure maximum flavor. With its rich, sweet notes and subtle smokiness, this natural spice delivers a delightful punch that enhances everything from savory stews and roasted meats to vibrant vegetable dishes and sauces.\n\nNot only is our Paprika a feast for the eyes with its brilliant red hue, but it's also packed with antioxidants and vitamins, making it a nutritious choice for health-conscious cooks. Whether you sprinkle it onto a beloved family recipe or use it to create something intentionally new, our Paprika is versatile enough to brighten any meal.\n\nTransform everyday cooking into an extraordinary experience with the irresistible"
}
```
