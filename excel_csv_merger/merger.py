"""Excel/CSVファイルの結合・集計ロジック"""
from pathlib import Path

import pandas as pd

ENCODINGS = ("utf-8-sig", "cp932", "utf-8")


def read_table(path):
    """xlsx/csv を読み込んで DataFrame で返す。
    CSVは文字コードを自動判定(UTF-8 BOM付き/Shift_JIS系/UTF-8)"""
    p = Path(path)
    if p.suffix.lower() in (".xlsx", ".xls"):
        return pd.read_excel(p)
    for enc in ENCODINGS:
        try:
            return pd.read_csv(p, encoding=enc)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"{p.name}: 文字コードを判定できませんでした")


def merge_files(paths):
    """複数ファイルを縦結合。出典ファイル名列を付ける"""
    frames = []
    for path in paths:
        df = read_table(path)
        df["出典ファイル"] = Path(path).name
        frames.append(df)
    if not frames:
        raise ValueError("ファイルが選択されていません")
    return pd.concat(frames, ignore_index=True, sort=False)


def summarize(df, key_col):
    """key_col でグループ化し、数値列の合計と件数を返す"""
    if not key_col or key_col not in df.columns:
        raise ValueError("集計列を選択してください")
    num_cols = [c for c in df.select_dtypes("number").columns
                if c != key_col]
    g = df.groupby(key_col, dropna=False)
    out = g[num_cols].sum() if num_cols else pd.DataFrame(
        index=g.size().index)
    out.insert(0, "件数", g.size())
    return out.reset_index()


def write_output(df_merged, df_sum, out_path):
    """結合データと集計結果を2シートのxlsxに出力"""
    with pd.ExcelWriter(out_path, engine="openpyxl") as w:
        df_merged.to_excel(w, sheet_name="結合データ", index=False)
        if df_sum is not None:
            df_sum.to_excel(w, sheet_name="集計", index=False)
