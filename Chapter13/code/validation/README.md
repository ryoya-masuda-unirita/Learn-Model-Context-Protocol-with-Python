# サンプルの実行

## 環境のセットアップ

[uv](https://docs.astral.sh/uv/) で依存関係をインストールします（初回のみ）。リポジトリ内のどのディレクトリで実行しても、リポジトリ直下の `.venv` にインストールされます：

```bash
uv sync
```

以降のコマンドは `uv run` を付けて実行します。仮想環境を有効化する必要はありません。

## サンプルの実行

```bash
uv run python pydantic_demo.py
```

次のような出力になります：

```text
pydantic のバージョン:  2.13.5
id=1 name='Dr. Smith' office_hours=[OfficeHour(day='月曜日', from_=9, to_=12), OfficeHour(day='水曜日', from_=14, to_=17)]
{'id': 1, 'name': 'Dr. Smith', 'office_hours': [{'day': '月曜日', 'from_': 9, 'to_': 12}, {'day': '水曜日', 'from_': 14, 'to_': 17}]}
```
