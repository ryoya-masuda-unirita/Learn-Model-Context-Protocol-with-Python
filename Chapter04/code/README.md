# サンプルの実行

## 仮想環境のセットアップ

```sh
python -m venv venv
source venv/bin/activate
```

## 依存関係のインストール

```bash
pip install "mcp[cli]"
```

## サーバーの実行

```sh
uvicorn server:app
```

## サーバーのテスト

```bash
mcp dev server.py
```

