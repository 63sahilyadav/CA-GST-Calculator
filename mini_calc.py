import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import os
import math
import requests

# --- GLOBAL VARIABLES & LOGIC ---
current_memory = 0.0

def save_entry(action, result):
    file_path = os.path.expanduser('~/python_projects/tax_log.csv')
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), action, result])

def calculate(event=None):
    try:
        val = entry.get()
        if not val: return
        res = eval(val.replace('^', '**'))
        label_res.config(text=f"Result: {res}")
        save_entry(f"Calc: {val}", res)
    except:
        messagebox.showerror("Error", "Invalid math")

def apply_gst(rate, reverse=False):
    try:
        val = float(entry.get())
        if reverse:
            base = val / (1 + (rate/100))
            total_tax = val - base
            half_tax = total_tax / 2
            res_text = f"Total: {val:.2f}\nBase: {base:.2f}\nCGST: {half_tax:.2f} | SGST: {half_tax:.2f}\nIGST: {total_tax:.2f}"
        else:
            total_tax = val * (rate/100)
            half_tax = total_tax / 2
            total_amt = val + total_tax
            res_text = f"Total: {total_amt:.2f}\nCGST: {half_tax:.2f} | SGST: {half_tax:.2f}\nIGST: {total_tax:.2f}"
        label_res.config(text=res_text)
        save_entry(f"GST {rate}%", res_text.replace('\n', ' '))
    except:
        messagebox.showerror("Error", "Enter a numeric value")

def convert_currency(target_curr):
    try:
        amount = float(entry.get())
        url = "https://open.er-api.com/v6/latest/INR"
        data = requests.get(url, timeout=5).json()
        if data["result"] == "success":
            rate = data["rates"][target_curr]
            converted = amount * rate
            label_res.config(text=f"{amount} INR = {converted:.2f} {target_curr}\n(Live Rate: {rate:.4f})")
    except:
        fallback = {"USD": 0.012, "EUR": 0.011, "GBP": 0.009, "AED": 0.044}
        rate = fallback.get(target_curr, 0)
        label_res.config(text=f"OFFLINE: {amount} INR ≈ {amount*rate:.2f} {target_curr}")

def open_history():
    history_win = tk.Toplevel(root)
    history_win.title("Audit Search")
    history_win.geometry("500x400")
    tk.Entry(history_win, width=40).pack(pady=10)
    tk.Listbox(history_win, width=60, height=15).pack(pady=10)

def clear_screen(event=None):
    entry.delete(0, tk.END)
    label_res.config(text="Result:")

# --- GUI INITIALIZATION ---
root = tk.Tk()
root.title("CA Pro Master: Tax, Finance & Forex")
root.geometry("600x950") # Expanded height to fit all tools

# Input Section
tk.Label(root, text="Financial Input / Formula:").pack(pady=5)
entry = tk.Entry(root, font=("Arial", 14), justify='center', width=40)
entry.pack(pady=5)
entry.focus_set()

tk.Button(root, text="Calculate (Enter)", command=calculate, bg="#E0E0E0", width=30).pack(pady=10)

# --- GRID LAYOUT FOR TOOLS ---
# Section 1: Memory & Finance
tools_frame = tk.Frame(root)
tools_frame.pack(pady=5)

for i, m in enumerate(["M+", "M-", "MR", "MC"]):
    tk.Button(tools_frame, text=m, width=8, bg="#607D8B", fg="white").grid(row=0, column=i, padx=2, pady=2)

for i, f in enumerate(["x^y", "√", "x²", "1/x"]):
    tk.Button(tools_frame, text=f, width=8, bg="#FF9800").grid(row=1, column=i, padx=2, pady=2)

# Section 2: Forex Converter
tk.Label(root, text="Forex Converter (INR to Foreign):", font=("Arial", 9, "bold")).pack()
fx_frame = tk.Frame(root)
fx_frame.pack(pady=5)
for i, curr in enumerate(["USD", "EUR", "GBP", "AED"]):
    tk.Button(fx_frame, text=curr, command=lambda c=curr: convert_currency(c), width=8, bg="#5C6BC0", fg="white").grid(row=0, column=i, padx=2)

# Section 3: Professional GST Slabs
gst_main_frame = tk.LabelFrame(root, text="GST TAX SLABS (Split CGST/SGST/IGST)")
gst_main_frame.pack(pady=10, padx=20, fill="x")

for i, rate in enumerate([5, 12, 18, 28]):
    tk.Button(gst_main_frame, text=f"{rate}%", command=lambda r=rate: apply_gst(r), bg="#2E7D32", fg="white", width=12).grid(row=i, column=0, padx=10, pady=2)
    tk.Button(gst_main_frame, text=f"Rev {rate}%", command=lambda r=rate: apply_gst(r, True), bg="#6A1B9A", fg="white", width=12).grid(row=i, column=1, padx=10, pady=2)

# Section 4: Audit Tools
tk.Button(root, text="Clear Screen (Esc)", command=clear_screen, bg="#f44336", fg="white", width=35).pack(pady=5)
tk.Button(root, text="View Audit Log (Search)", command=open_history, bg="#546E7A", fg="white", width=35).pack(pady=2)
tk.Button(root, text="Monthly Tax Summary", bg="#388E3C", fg="white", width=35).pack(pady=2)

# Result Area (Anchored at the bottom)
label_res = tk.Label(root, text="Result:", font=("Arial", 12, "bold"), fg="#1565C0", justify="left")
label_res.pack(pady=20)

# --- KEYBOARD BINDINGS ---
root.bind('<Return>', calculate)
root.bind('<Escape>', clear_screen)
for i, r in enumerate([5, 12, 18, 28]):
    root.bind(f'<F{i+1}>', lambda e, rate=r: apply_gst(rate))
    root.bind(f'<Alt-F{i+1}>', lambda e, rate=r: apply_gst(rate, True))

root.mainloop()