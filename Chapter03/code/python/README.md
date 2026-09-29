# サンプルの実行

## 仮想環境のセットアップ

```bash
python -m venv venv
```

仮想環境を有効化します：

```bash
source venv/bin/activate
```

Windows の場合は次のように入力します：

```bash
venv\Scripts\activate
```

## 依存関係のインストール

```bash
pip install "mcp[cli]"
```

## コードの実行

```bash
mcp run server.py
```

## Inspector の実行

```bash
mcp dev server.py
```

Web 画面が開くはずです。次のように選択してください：

- transport は "stdio"
- command：**mcp**
- arguments：**run server.py**

その後、"Connect" ボタンを押します。
