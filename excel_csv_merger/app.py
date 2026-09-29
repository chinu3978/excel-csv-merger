"""Excel/CSV結合・集計ツール GUI

使い方:
  python app.py

1. 「ファイル追加」で xlsx/csv を複数選択
2. 集計キー列を選択(任意。空なら結合だけ行う)
3. 「結合して保存」で出力先を指定して実行
"""
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import merger

FILETYPES = [("Excel/CSV", "*.xlsx;*.xls;*.csv"), ("すべて", "*.*")]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Excel/CSV 結合・集計ツール")
        self.geometry("560x420")
        self.minsize(480, 360)
        self.paths = []
        self._build()

    def _build(self):
        pad = {"padx": 10, "pady": 4}

        ttk.Label(self, text="結合するファイルを追加してください",
                  font=("", 11, "bold")).pack(anchor="w", **pad)

        body = ttk.Frame(self)
        body.pack(fill="both", expand=True, **pad)

        self.listbox = tk.Listbox(body, activestyle="none")
        sb = ttk.Scrollbar(body, orient="vertical",
                           command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=sb.set)
        self.listbox.pack(side="left", fill="both", expand=True)
        sb.pack(side="left", fill="y")

        btns = ttk.Frame(body)
        btns.pack(side="left", fill="y", padx=(8, 0))
        ttk.Button(btns, text="ファイル追加",
                   command=self.on_add).pack(fill="x", pady=2)
        ttk.Button(btns, text="選択を削除",
                   command=self.on_remove).pack(fill="x", pady=2)
        ttk.Button(btns, text="クリア",
                   command=self.on_clear).pack(fill="x", pady=2)

        row = ttk.Frame(self)
        row.pack(fill="x", **pad)
        ttk.Label(row, text="集計キー列(任意):").pack(side="left")
        self.key_var = tk.StringVar()
        self.key_box = ttk.Combobox(row, textvariable=self.key_var,
                                    state="readonly", width=24)
        self.key_box.pack(side="left", padx=6)
        ttk.Label(row, text="※選ぶと列ごとの合計・件数も出力",
                  foreground="#666").pack(side="left")

        ttk.Button(self, text="結合して保存",
                   command=self.on_run).pack(**pad)

        self.status = ttk.Label(self, text="待機中", foreground="#555")
        self.status.pack(anchor="w", **pad)

    def on_add(self):
        files = filedialog.askopenfilenames(
            title="結合するファイルを選択", filetypes=FILETYPES)
        for f in files:
            if f not in self.paths:
                self.paths.append(f)
                self.listbox.insert("end", Path(f).name)
        if files:
            self._load_columns()

    def on_remove(self):
        for i in reversed(self.listbox.curselection()):
            self.listbox.delete(i)
            del self.paths[i]

    def on_clear(self):
        self.listbox.delete(0, "end")
        self.paths.clear()
        self.key_box["values"] = []
        self.key_var.set("")
        self._set_status("待機中")

    def _load_columns(self):
        try:
            df = merger.read_table(self.paths[0])
        except Exception as e:
            messagebox.showwarning("読み込み警告", str(e))
            return
        self.key_box["values"] = [""] + list(df.columns)
        self._set_status(f"{len(self.paths)} 件のファイルを選択中"
                         f"  (先頭: {len(df)} 行)")

    def on_run(self):
        if not self.paths:
            messagebox.showinfo("確認", "ファイルを追加してください")
            return
        out = filedialog.asksaveasfilename(
            title="出力先を指定", defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
            initialfile="結合結果.xlsx")
        if not out:
            return
        try:
            df = merger.merge_files(self.paths)
            key = self.key_var.get()
            summary = merger.summarize(df, key) if key else None
            merger.write_output(df, summary, out)
        except Exception as e:
            messagebox.showerror("エラー", str(e))
            self._set_status("エラー: 出力できませんでした")
            return
        self._set_status(f"完了: {out} ({len(df)} 行)")
        messagebox.showinfo("完了", f"{len(df)} 行を出力しました\n{out}")

    def _set_status(self, text):
        self.status.configure(text=text)


if __name__ == "__main__":
    App().mainloop()
