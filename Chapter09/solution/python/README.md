## サンプルの実行

課題の解答です。

## 環境のセットアップ

[uv](https://docs.astral.sh/uv/) で依存関係をインストールします（初回のみ）。リポジトリ内のどのディレクトリで実行しても、リポジトリ直下の `.venv` にインストールされます：

```bash
uv sync
```

以降のコマンドは `uv run` を付けて実行します。仮想環境を有効化する必要はありません。

## 実行

このサンプルは、LLM として Amazon Bedrock の GPT-5.5（モデル ID `openai.gpt-5.5`、リージョン us-east-1）を、OpenAI 互換 API で呼び出します。実行には次のものが必要です：

- Bedrock を使える AWS の認証情報（`aws configure` などで設定したプロファイル）
- Bedrock で OpenAI の GPT-5.5 が使える状態になっていること

Bedrock の API キーは、実行時に AWS の認証情報から短期トークンを自動で作るので、別途発行する必要はありません。使うプロファイルは環境変数 `AWS_PROFILE` で指定します。

次のコマンドで実行します（`<プロファイル名>` は自分の AWS のプロファイル名に置き換えます）：

```sh
AWS_PROFILE=<プロファイル名> uv run python client.py
```

LLM が characters.json のキャラクターになりきって応答し、次のような結果になります（生成される文章は実行するたびに変わります。クライアントの max_tokens が 200 なので、途中で切れます）：

```text
サンプリングのリクエスト: [SamplingMessage(role='user', content=TextContent(type='text', text='Monsieur Lestrange と話してください。話題は「あなた自身について教えて」です。', annotations=None, meta=None), meta=None)]
結果: ああ、これはこれは。ご丁寧にありがとうございます。

わたくしは **Monsieur Lestrange** と申します。六百年ほど生きております吸血鬼でして、まあ……世間では「古き夜の貴族」などと勝手に呼ばれることもありますが、実情はもっと地味なものです。

たとえば、皆さまは吸血鬼と聞くと、棺、満月、霧の中の古城、あるいは勇敢な吸血鬼ハンターとの死闘などを想像なさるでしょう。ええ、そういうものも多少はございます。しかし、
```
