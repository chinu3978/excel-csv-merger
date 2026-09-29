# Excel/CSV 結合・集計ツール

複数の Excel(.xlsx/.xls)・CSV ファイルをまとめて読み込み、
1つの表に結合したうえで、指定した列ごとの合計・件数の集計表を
出力する GUI ツールです。

![screenshot](screenshot.png)

## 機能

- 複数ファイルの一括結合(xlsx / csv 混在OK)
- CSV の文字コード自動判定(UTF-8 / Shift_JIS 系)
- どのファイル由来か分かる「出典ファイル」列を自動付与
- 任意の列をキーにした集計(数値列の合計 + 件数)
- 出力は1つの Excel ファイル(結合データ / 集計 の2シート)

## 使い方

```
pip install -r requirements.txt
python app.py
```

1. 「ファイル追加」で対象ファイルを複数選択
2. 集計キー列を選択(空欄なら結合のみ)
3. 「結合して保存」で出力先を指定

## デモデータ

```
python sample_data.py
```

`sample/` に支店別の売上CSV(Shift_JIS)を生成し、
結合・集計の動作確認を行います。

## 構成

- `app.py` — GUI(tkinter)
- `merger.py` — 結合・集計・出力ロジック(pandas)
- `sample_data.py` — デモデータ生成と動作確認
