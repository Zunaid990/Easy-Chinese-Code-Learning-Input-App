# import pandas as pd
# import numpy as np
# import tkinter as tk
# from tkinter import messagebox

# root = tk.Tk()
# root.title("ecc")
# root.geometry("300x200")

# entry = tk.Entry(root)
# entry.pack(pady=10)

# output = tk.Label(root, text="", fg="blue")
# output.pack(pady=10)


# df = pd.read_csv("data.csv")
# df = df[['character', 'voice_code', '1', '2', '3']]


# def return_ecc():
#     input_arr = np.array(list(entry.get()))
#     dimensions = df.shape
#     for i in range(0, dimensions[1]):
#         result = (df.iloc[i][1:len(input_arr) + 1] == input_arr).all()
#         if result:
#             print(df.iloc[i, 0])
#             output.config(text=df.iloc[i, 0])


# button = tk.Button(root, text="submit", command=return_ecc)
# button.pack(pady=10)

# root.mainloop()

import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox


# Load dataset

try:
    df = pd.read_csv("data.csv")
except Exception as e:
    messagebox.showerror("Load Error", f"Could not read data.csv\n{e}")
    raise


df = df[['character', 'voice_code', '1', '2', '3']].copy()


def _norm(s): return str(s).strip().lower()


df["_prefix"] = df[['1', '2', '3']].astype(str).agg(''.join, axis=1).map(_norm)


#  core logic


def core_return_ecc(user_text: str, out_label: tk.Label, vc_label: tk.Label, status_var: tk.StringVar):
    """
    Your original algorithm: compare typed chars against columns 1..N of each row.
    Only fix: iterate over ROWS (df.shape[0]) instead of columns.
    """
    input_arr = np.array(list(user_text))
    dims = df.shape  # (rows, cols)

    found_char = None
    found_voice = None

    # iterate over rows
    for i in range(0, dims[0]):

        try:

            row_slice = df.iloc[i][1:len(input_arr) + 1]
            result = (row_slice.values == input_arr).all()
        except Exception:
            result = False

        if result:
            found_char = df.iloc[i, 0]
            found_voice = df.iloc[i, 1]
            break

    if found_char:
        out_label.config(text=found_char)
        vc_label.config(text=f"voice_code: {found_voice}")
        status_var.set("Exact match found.")
    else:
        out_label.config(text="—")
        vc_label.config(text="voice_code: —")
        status_var.set(
            "No exact match. Try more letters or pick a prefix candidate.")


# GUI

class ECCApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ECC — Easy Chinese Code")
        self.geometry("560x460")
        self.minsize(540, 440)

        # style
        try:
            self.style = ttk.Style(self)
            if "vista" in self.style.theme_names():
                self.style.theme_use("vista")
        except Exception:
            pass

        # header
        ttk.Label(self, text="ECC: Easy Chinese Code", font=(
            "Segoe UI", 16, "bold")).pack(pady=(10, 0))
        ttk.Label(self, text="Type letters that correspond to the ECC columns; see exact & prefix matches.",
                  foreground="#666").pack(pady=(0, 8))

        # input frame
        inp = ttk.LabelFrame(self, text="Input")
        inp.pack(fill="x", padx=12, pady=6)
        row = ttk.Frame(inp)
        row.pack(fill="x", padx=10, pady=8)
        ttk.Label(row, text="Code:").pack(side="left")
        self.entry = ttk.Entry(row, width=30)
        self.entry.pack(side="left", padx=8, expand=True, fill="x")
        self.entry.bind("<Return>", self.on_submit)
        self.entry.bind("<KeyRelease>", self.on_type)

        ttk.Button(row, text="Submit (Enter)",
                   command=self.on_submit).pack(side="left", padx=4)
        ttk.Button(row, text="Clear",
                   command=self.clear_input).pack(side="left")

        # results frame
        res = ttk.LabelFrame(self, text="Results")
        res.pack(fill="both", expand=True, padx=12, pady=6)

        # exact
        ttk.Label(res, text="✓ Exact Match", font=("Segoe UI", 11, "bold")).pack(
            anchor="w", padx=10, pady=(8, 0))
        self.lbl_char = ttk.Label(res, text="—", font=("Segoe UI", 30))
        self.lbl_char.pack(anchor="w", padx=20)
        self.lbl_voice = ttk.Label(res, text="voice_code: —")
        self.lbl_voice.pack(anchor="w", padx=22, pady=(0, 6))

        # prefix list
        ttk.Label(res, text="▷ Prefix Matches (Top 15)", font=(
            "Segoe UI", 11, "bold")).pack(anchor="w", padx=10)
        self.listbox = tk.Listbox(res, height=10)
        self.listbox.pack(fill="both", expand=True, padx=18, pady=(2, 10))
        self.listbox.bind("<Double-Button-1>", self.pick_from_list)
        self.listbox.bind("<Return>", self.pick_from_list)

        # bottom controls
        bottom = ttk.Frame(self)
        bottom.pack(fill="x", padx=12, pady=(0, 8))
        ttk.Button(bottom, text="Copy Character",
                   command=self.copy_char).pack(side="left")
        ttk.Label(
            bottom, text="(Double-click a candidate to choose)").pack(side="right")

        # status bar
        self.status = tk.StringVar(
            value=f"Loaded {len(df)} rows from data.csv  |  Columns: character, voice_code, 1, 2, 3")
        ttk.Label(self, textvariable=self.status, relief="sunken",
                  anchor="w").pack(fill="x", side="bottom")

        # initial fill
        self.refresh_prefix_list("")

    # --- events ---
    def on_submit(self, _evt=None):
        text = self.entry.get().strip()
        if not text:
            messagebox.showinfo("Input", "Type some letters first.")
            return
        core_return_ecc(text, self.lbl_char, self.lbl_voice, self.status)

    def on_type(self, _evt=None):
        self.refresh_prefix_list(self.entry.get())

    def pick_from_list(self, _evt=None):
        sel = self.listbox.get(tk.ACTIVE)
        if not sel:
            return
        # ‘code → char (voice)’ format
        try:
            code_part, right = sel.split("→", 1)
            code_part = code_part.strip()
            char_part = right.strip().split()[0]
        except Exception:
            char_part = sel.strip()
        self.lbl_char.config(text=char_part)
        # voice_code from df
        vc = "—"
        row = df[df['character'].astype(str) == char_part]
        if not row.empty:
            vc = row.iloc[0]['voice_code']
        self.lbl_voice.config(text=f"voice_code: {vc}")
        self.status.set(f"Chosen: {char_part}")

    def copy_char(self):
        ch = self.lbl_char.cget("text")
        if not ch or ch == "—":
            self.status.set("Nothing to copy.")
            return
        self.clipboard_clear()
        self.clipboard_append(ch)
        self.status.set(f"Copied: {ch}")

    def clear_input(self):
        self.entry.delete(0, tk.END)
        self.lbl_char.config(text="—")
        self.lbl_voice.config(text="voice_code: —")
        self.refresh_prefix_list("")
        self.status.set("Cleared.")

    # --- prefix list logic (extra feature, non-invasive) ---
    def refresh_prefix_list(self, raw_text: str):
        q = _norm(raw_text)
        self.listbox.delete(0, tk.END)
        if not q:
            # show top few by dataset order
            subset = df.head(15)
        else:
            # startswith on our concatenated prefix key
            subset = df[df["_prefix"].str.startswith(q)].head(15)
        for _, r in subset.iterrows():
            code_str = f"{str(r['1'])}{str(r['2'])}{str(r['3'])}"
            disp = f"{code_str:<8} → {r['character']}   ({r['voice_code']})"
            self.listbox.insert(tk.END, disp)


if __name__ == "__main__":
    app = ECCApp()
    app.mainloop()
