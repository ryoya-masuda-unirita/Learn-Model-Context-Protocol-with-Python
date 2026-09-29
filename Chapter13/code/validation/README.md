# サンプルの実行

## インストール

正しいバージョンの Pydantic がインストールされていることを確認してください。pip でインストールできます：

```sh
pip install pydantic==2.5.3
```

## サンプルの実行

```powershell
python .\pydantic_demo.py
```

次のような出力になります：

```text
pydantic のバージョン:  2.5.3
id=1 name='Dr. Smith' office_hours=[OfficeHour(day='月曜日', from_=9, to_=12), OfficeHour(day='水曜日', from_=14, to_=17)]
{'id': 1, 'name': 'Dr. Smith', 'office_hours': [{'day': '月曜日', 'from_': 9, 'to_': 12}, {'day': '水曜日', 'from_': 14, 'to_': 17}]}
```
