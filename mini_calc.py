import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import os
import math

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

def apply_percent():
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
    except:
        messagebox.showerror("Error", "Use format: Value * Percent")

def toggle_sign():
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

def finance_op(op):
    try:
        val = float(entry.get())
        if op == "sqrt": res = math.sqrt(val)
        elif op == "sq": res = val ** 2
        label_res.config(text=f"Result: {res}")
    except:
        messagebox.showerror("Error", "Enter a number first")

def memory_op(op):
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

def clear_screen(event=None):
    entry.delete(0, tk.END)
    label_res.config(text="Result: ")

# GUI Construction
root = tk.Tk()
root.title("CA Pro: GST & Financial Calculator")
root.geometry("480x880")

tk.Label(root, text="Financial Input / Formula:", font=("Arial", 10)).pack(pady=10)
entry = tk.Entry(root, font=("Arial", 14), justify='center')
entry.pack(pady=5, padx=20, fill='x')

tk.Button(root, text="Calculate (Enter)", command=calculate, height=2, width=35, bg="#E0E0E0").pack(pady=10)

# 1. Standard Tools Row
tk.Label(root, text="Standard Tools:", font=("Arial", 9, "bold")).pack()
std_frame = tk.Frame(root); std_frame.pack(pady=5)
tk.Button(std_frame, text="%", command=apply_percent, width=9, height=2, bg="#CFD8DC").grid(row=0, column=0, padx=2)
tk.Button(std_frame, text="+/-", command=toggle_sign, width=9, height=2, bg="#CFD8DC").grid(row=0, column=1, padx=2)
tk.Button(std_frame, text="(", command=lambda: entry.insert(tk.END, "("), width=9, height=2, bg="#CFD8DC").grid(row=0, column=2, padx=2)
tk.Button(std_frame, text=")", command=lambda: entry.insert(tk.END, ")"), width=9, height=2, bg="#CFD8DC").grid(row=0, column=3, padx=2)

# 2. Memory Row
tk.Label(root, text="Memory Functions:", font=("Arial", 9, "bold")).pack()
mem_frame = tk.Frame(root); mem_frame.pack(pady=5)
for i, m_op in enumerate(["M+", "M-", "MR", "MC"]):
    tk.Button(mem_frame, text=m_op, command=lambda o=m_op: memory_op(o), width=9, height=2, bg="#607D8B", fg="white").grid(row=0, column=i, padx=2)

# 3. Finance Row (TVM)
tk.Label(root, text="Finance Ops (TVM):", font=("Arial", 9, "bold")).pack()
fin_frame = tk.Frame(root); fin_frame.pack(pady=5)
tk.Button(fin_frame, text="x^y", command=lambda: entry.insert(tk.END, "^"), width=9, height=2, bg="#FF9800").grid(row=0, column=0, padx=2)
tk.Button(fin_frame, text="√", command=lambda: finance_op("sqrt"), width=9, height=2, bg="#FF9800").grid(row=0, column=1, padx=2)
tk.Button(fin_frame, text="x²", command=lambda: finance_op("sq"), width=9, height=2, bg="#FF9800").grid(row=0, column=2, padx=2)
tk.Button(fin_frame, text="1/x", command=lambda: entry.insert(0, "1/(")+entry.insert(tk.END, ")"), width=9, height=2, bg="#FF9800").grid(row=0, column=3, padx=2)

# 4. Professional GST Split Row
tk.Label(root, text="GST TAX SLABS (Split CGST/SGST/IGST):", font=("Arial", 9, "bold")).pack(pady=5)
f_frame = tk.Frame(root); f_frame.pack()
r_frame = tk.Frame(root); r_frame.pack(pady=5)
rates = [5, 12, 18, 28]
for i, rate in enumerate(rates):
    tk.Button(f_frame, text=f"{rate}%", command=lambda r=rate: apply_gst(r), bg="#2E7D32", fg="white", width=9, height=2).grid(row=0, column=i, padx=2)
    tk.Button(r_frame, text=f"Rev {rate}%", command=lambda r=rate: apply_gst(r, True), bg="#6A1B9A", fg="white", width=9, height=2).grid(row=0, column=i, padx=2)

tk.Button(root, text="Clear Screen (Esc)", command=clear_screen, bg="#f44336", fg="white", height=2, width=35).pack(pady=15)
label_res = tk.Label(root, text="Result: ", font=("Arial", 11, "bold"), fg="#1565C0", justify="left")
label_res.pack(pady=10)

# --- RESTORED ALL KEYBOARD BINDINGS ---
entry.focus_force()
root.bind('<Return>', calculate)
root.bind('<KP_Enter>', calculate)
root.bind('<Escape>', clear_screen)
root.bind('<F1>', lambda e: apply_gst(5))
root.bind('<F2>', lambda e: apply_gst(12))
root.bind('<F3>', lambda e: apply_gst(18))
root.bind('<F4>', lambda e: apply_gst(28))
root.bind('<Alt-F1>', lambda e: apply_gst(5, True))
root.bind('<Alt-F2>', lambda e: apply_gst(12, True))
root.bind('<Alt-F3>', lambda e: apply_gst(18, True))
root.bind('<Alt-F4>', lambda e: apply_gst(28, True))

root.mainloop()