import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import os
import math
import requests

# Global Memory Variable
current_memory = 0.0

def save_entry(action, result):
    """Logs every calculation for professional audit trails."""
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

def apply_percent(event=None):
    try:
        val = entry.get()
        if '*' in val:
            parts = val.split('*')
            res = float(parts[0]) * (float(parts[1]) / 100)
        else:
            res = float(val) / 100
        entry.delete(0, tk.END)
        entry.insert(0, str(res))
        label_res.config(text=f"Result: {res}")
    except: pass

def toggle_sign(event=None):
    try:
        val = entry.get()
        if val.startswith('-'): entry.delete(0, 1)
        else: entry.insert(0, '-')
    except: pass

def apply_gst(rate, reverse=False):
    try:
        val = float(entry.get())
        if reverse:
            base = val / (1 + (rate/100))
            total_tax = val - base
            half_tax = total_tax / 2
            label_res.config(text=f"Base: {base:.2f}\nCGST: {half_tax:.2f} | SGST: {half_tax:.2f}\nIGST: {total_tax:.2f}")
            save_entry(f"Rev {rate}% on {val}", f"Base: {base:.2f}")
        else:
            total_tax = val * (rate/100)
            half_tax = total_tax / 2
            total_amt = val + total_tax
            label_res.config(text=f"Total: {total_amt:.2f}\nCGST: {half_tax:.2f} | SGST: {half_tax:.2f}\nIGST: {total_tax:.2f}")
            save_entry(f"Fwd {rate}% on {val}", f"Total: {total_amt:.2f}")
    except:
        messagebox.showerror("Error", "Enter a numeric value")

def finance_op(op, event=None):
    try:
        val = float(entry.get())
        if op == "sqrt": res = math.sqrt(val)
        elif op == "sq": res = val ** 2
        label_res.config(text=f"Result: {res}")
    except: pass

def memory_op(op, event=None):
    global current_memory
    try:
        if op == "MR":
            entry.delete(0, tk.END)
            entry.insert(0, str(current_memory))
            return
        val = float(entry.get())
        if op == "M+": current_memory += val
        elif op == "M-": current_memory -= val
        elif op == "MC": current_memory = 0.0
        label_res.config(text=f"Memory: {current_memory:.2f}")
    except:
        if op == "MC": current_memory = 0.0; label_res.config(text="Memory Cleared")

def convert_currency(target_curr="USD"):
    try:
        amount = float(entry.get())
        url = "https://open.er-api.com/v6/latest/INR"
        data = requests.get(url).json()
        if data["result"] == "success":
            rate = data["rates"][target_curr]
            converted = amount * rate
            label_res.config(text=f"{amount} INR = {converted:.2f} {target_curr}\n(Live Rate: {rate:.4f})")
            save_entry(f"Forex {target_curr}", f"{converted:.2f}")
    except:
        messagebox.showerror("Forex Error", "Internet needed for live rates.")

def open_history():
    history_win = tk.Toplevel(root)
    history_win.title("Tax Audit Log - Search")
    history_win.geometry("500x450")
    tk.Label(history_win, text="Search Audit Log (Keyword/Date):", font=("Arial", 10, "bold")).pack(pady=5)
    search_entry = tk.Entry(history_win, width=40)
    search_entry.pack(pady=5)
    listbox = tk.Listbox(history_win, width=60, height=15)
    listbox.pack(pady=10, padx=10)
    def perform_search():
        listbox.delete(0, tk.END)
        query = search_entry.get().lower()
        file_path = os.path.expanduser('~/python_projects/tax_log.csv')
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                for line in f:
                    if query in line.lower(): listbox.insert(tk.END, line.strip())
    tk.Button(history_win, text="Search", command=perform_search, bg="#607D8B", fg="white").pack()

def show_monthly_summary():
    summary_win = tk.Toplevel(root)
    summary_win.title("Monthly Summary")
    summary_win.geometry("400x300")
    tk.Label(summary_win, text="Enter Month (YYYY-MM):", font=("Arial", 10)).pack(pady=10)
    month_entry = tk.Entry(summary_win)
    month_entry.insert(0, datetime.now().strftime("%Y-%m-%d")[:7])
    month_entry.pack(pady=5)
    res_label = tk.Label(summary_win, text="", font=("Arial", 11, "bold"), fg="#2E7D32")
    res_label.pack(pady=20)
    def calculate_summary():
        target, total_vol = month_entry.get(), 0.0
        file_path = os.path.expanduser('~/python_projects/tax_log.csv')
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0].startswith(target) and "Total:" in row[2]:
                        try: total_vol += float(row[2].split("Total:")[1].strip())
                        except: continue
            res_label.config(text=f"Total Volume for {target}: ₹{total_vol:.2f}")
    tk.Button(summary_win, text="Summarize", command=calculate_summary, bg="#2E7D32", fg="white").pack()

def clear_screen(event=None):
    entry.delete(0, tk.END)
    label_res.config(text="Result: ")

# GUI Layout
root = tk.Tk()
root.title("CA Pro Master: Tax, Finance & Forex")
root.geometry("480x1050")

entry = tk.Entry(root, font=("Arial", 14), justify='center')
entry.pack(pady=20, padx=20, fill='x')

# Execution
tk.Button(root, text="Calculate (Enter)", command=calculate, height=2, width=35, bg="#E0E0E0").pack()

# Standard Tools
std_frame = tk.Frame(root); std_frame.pack(pady=10)
for i, (txt, cmd) in enumerate([("%", apply_percent), ("+/-", toggle_sign)]):
    tk.Button(std_frame, text=txt, command=cmd, width=9, height=2, bg="#CFD8DC").grid(row=0, column=i, padx=2)
tk.Button(std_frame, text="(", command=lambda: entry.insert(tk.END, "("), width=9, height=2, bg="#CFD8DC").grid(row=0, column=2, padx=2)
tk.Button(std_frame, text=")", command=lambda: entry.insert(tk.END, ")"), width=9, height=2, bg="#CFD8DC").grid(row=0, column=3, padx=2)

# Memory
tk.Label(root, text="Memory Functions:", font=("Arial", 9, "bold")).pack()
mem_frame = tk.Frame(root); mem_frame.pack(pady=5)
for i, m_op in enumerate(["M+", "M-", "MR", "MC"]):
    tk.Button(mem_frame, text=m_op, command=lambda o=m_op: memory_op(o), width=9, height=2, bg="#607D8B", fg="white").grid(row=0, column=i, padx=2)

# Finance
tk.Label(root, text="Finance Ops (TVM):", font=("Arial", 9, "bold")).pack()
fin_frame = tk.Frame(root); fin_frame.pack(pady=5)
tk.Button(fin_frame, text="x^y", command=lambda: entry.insert(tk.END, "^"), width=9, height=2, bg="#FF9800").grid(row=0, column=0, padx=2)
tk.Button(fin_frame, text="√", command=lambda: finance_op("sqrt"), width=9, height=2, bg="#FF9800").grid(row=0, column=1, padx=2)
tk.Button(fin_frame, text="x²", command=lambda: finance_op("sq"), width=9, height=2, bg="#FF9800").grid(row=0, column=2, padx=2)
tk.Button(fin_frame, text="1/x", command=lambda: entry.insert(0, "1/(")+entry.insert(tk.END, ")"), width=9, height=2, bg="#FF9800").grid(row=0, column=3, padx=2)

# Forex (NEW)
tk.Label(root, text="Forex Converter (INR to Foreign):", font=("Arial", 9, "bold")).pack(pady=5)
fx_frame = tk.Frame(root); fx_frame.pack()
for i, curr in enumerate(["USD", "EUR", "GBP", "AED"]):
    tk.Button(fx_frame, text=curr, command=lambda c=curr: convert_currency(c), width=9, height=2, bg="#5C6BC0", fg="white").grid(row=0, column=i, padx=2)

# GST Slabs
tk.Label(root, text="GST TAX SLABS (Split CGST/SGST/IGST):", font=("Arial", 9, "bold")).pack(pady=5)
f_frame = tk.Frame(root); f_frame.pack()
r_frame = tk.Frame(root); r_frame.pack(pady=5)
for i, rate in enumerate([5, 12, 18, 28]):
    tk.Button(f_frame, text=f"{rate}%", command=lambda r=rate: apply_gst(r), bg="#2E7D32", fg="white", width=9, height=2).grid(row=0, column=i, padx=2)
    tk.Button(r_frame, text=f"Rev {rate}%", command=lambda r=rate: apply_gst(r, True), bg="#6A1B9A", fg="white", width=9, height=2).grid(row=0, column=i, padx=2)

tk.Button(root, text="Clear Screen (Esc)", command=clear_screen, bg="#f44336", fg="white", height=2, width=35).pack(pady=10)

# Audit
tk.Button(root, text="View Audit Log (Search)", command=open_history, bg="#546E7A", fg="white", width=35).pack(pady=5)
tk.Button(root, text="Monthly Tax Summary", command=show_monthly_summary, bg="#388E3C", fg="white", width=35).pack(pady=5)

label_res = tk.Label(root, text="Result: ", font=("Arial", 11, "bold"), fg="#1565C0", justify="left")
label_res.pack(pady=10)

# Keyboard Bindings
entry.focus_force()
root.bind('<Return>', calculate); root.bind('<KP_Enter>', calculate); root.bind('<Escape>', clear_screen)
root.bind('<percent>', apply_percent); root.bind('<Control-s>', toggle_sign)
root.bind('<Alt-p>', lambda e: memory_op("M+")); root.bind('<Alt-m>', lambda e: memory_op("M-"))
root.bind('<Alt-r>', lambda e: memory_op("MR")); root.bind('<Alt-c>', lambda e: memory_op("MC"))
root.bind('<Control-q>', lambda e: finance_op("sqrt")); root.bind('<Control-w>', lambda e: finance_op("sq"))
root.bind('<Control-p>', lambda e: entry.insert(tk.END, "^"))
for i, r in enumerate([5, 12, 18, 28]):
    root.bind(f'<F{i+1}>', lambda e, rate=r: apply_gst(rate))
    root.bind(f'<Alt-F{i+1}>', lambda e, rate=r: apply_gst(rate, True))

root.mainloop()