## サンプルの実行

課題の解答です。

## 環境のセットアップ

[uv](https://docs.astral.sh/uv/) で依存関係をインストールします（初回のみ）。リポジトリ内のどのディレクトリで実行しても、リポジトリ直下の `.venv` にインストールされます：

```bash
uv sync
```

以降のコマンドは `uv run` を付けて実行します。仮想環境を有効化する必要はありません。

## 実行

次のコマンドで実行します：

```sh
uv run python client.py
```

次のような結果になります：

```text
結果: Ah, bonsoir, my dear interlocutor! It is a pleasure to make your acquaintance. As you may have surmised, I am Monsieur Lestrange, a vampire of some six centuries in age. One could say that I have had ample time to observe the intricacies of life, even from the peculiar vantage of my somewhat... unique existence.

However, if I must indulge in the topic of "me," I find it rather tedious when compared to the perennial tribulation of managing a magnificent yet drafty castle. You see, my abode, a resplendent structure that has stood the test of time for more than a millennium, possesses an architectural charm that is unfortunately accompanied by the inefficiencies of medieval insulation.

Ah, the electricity bill! It is a bane of my existence, I assure you. The monthly accumulation of expenses tends to escalate, particularly during the colder months when I find myself resorting to those ghastly electrical heaters to combat the chill that seeps through the
```
