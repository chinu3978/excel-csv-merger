"""デモ用サンプルCSV生成 + ロジックの動作確認
python sample_data.py → sample/ に支店別CSVを生成し、結合テストを実行"""
import csv
from pathlib import Path

import merger

SAMPLE_DIR = Path(__file__).parent / "sample"

ROWS = {
    "1月_東京.csv": [
        ["日付", "支店", "商品", "数量", "金額"],
        ["2025-01-05", "東京", "商品A", "12", "36000"],
        ["2025-01-12", "東京", "商品B", "7", "21000"],
        ["2025-01-20", "東京", "商品A", "5", "15000"],
    ],
    "2月_大阪.csv": [
        ["日付", "支店", "商品", "数量", "金額"],
        ["2025-02-03", "大阪", "商品A", "20", "60000"],
        ["2025-02-15", "大阪", "商品C", "3", "9000"],
        ["2025-02-22", "大阪", "商品B", "11", "33000"],
    ],
    "3月_名古屋.csv": [
        ["日付", "支店", "商品", "数量", "金額"],
        ["2025-03-08", "名古屋", "商品B", "9", "27000"],
        ["2025-03-19", "名古屋", "商品A", "15", "45000"],
    ],
}


def make_samples():
    SAMPLE_DIR.mkdir(exist_ok=True)
    for name, rows in ROWS.items():
        with open(SAMPLE_DIR / name, "w", newline="",
                  encoding="cp932") as f:
            csv.writer(f).writerows(rows)
    print(f"sample/ に {len(ROWS)} 件のCSVを生成しました(Shift_JIS)")


def selftest():
    paths = sorted(SAMPLE_DIR.glob("*.csv"))
    df = merger.merge_files(paths)
    print(f"結合: {len(df)} 行 / 列: {list(df.columns)}")
    s = merger.summarize(df, "支店")
    print("支店別集計:")
    print(s.to_string(index=False))
    s2 = merger.summarize(df, "商品")
    print("商品別集計:")
    print(s2.to_string(index=False))
    out = SAMPLE_DIR / "結合結果_テスト.xlsx"
    merger.write_output(df, s, out)
    print(f"出力OK: {out}")


if __name__ == "__main__":
    make_samples()
    selftest()
