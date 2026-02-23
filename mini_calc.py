import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import os
import math

# Global Memory Variable
current_memory = 0.0

def save_entry(action, result):
    """Logs every calculation to a CSV for professional audit trails."""
    file_path = os.path.expanduser('~/python_projects/tax_log.csv')
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), action, result])

def calculate(event=None):
    try:
        val = entry.get()
        if not val: return
        # Supports ^ for power calculations like (1+r)^n
        res = eval(val.replace('^', '**'))
        label_res.config(text=f"Result: {res}")
        save_entry(f"Calc: {val}", res)
    except Exception:
        messagebox.showerror("Error", "Invalid math")

def apply_gst(rate, reverse=False):
    try:
        val = float(entry.get())
        if reverse:
            base = val / (1 + (rate/100))
            tax = val - base
            label_res.config(text=f"Base: {base:.2f} | {rate}% GST: {tax:.2f}")
            save_entry(f"Reverse {rate}% GST on {val}", f"Base: {base:.2f}")
        else:
            tax = val * (rate/100)
            total = val + tax
            label_res.config(text=f"GST: {tax:.2f} | Total: {total:.2f}")
            save_entry(f"Forward {rate}% GST on {val}", f"Total: {total:.2f}")
    except ValueError:
        messagebox.showerror("Error", "Enter a numeric value")

def finance_op(op):
    try:
        val = float(entry.get())
        if op == "sqrt": res = math.sqrt(val)
        elif op == "sq": res = val ** 2
        label_res.config(text=f"Result: {res}")
    except ValueError:
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
    except ValueError:
        if op == "MC": 
            current_memory = 0.0
            label_res.config(text="Memory Cleared")
        else:
            messagebox.showerror("Error", "Input needed for Memory Op")

def clear_screen(event=None):
    entry.delete(0, tk.END)
    label_res.config(text="Result: ")

# GUI Construction
root = tk.Tk()
root.title("CA Finalist Pro Financial Calc")
root.geometry("460x700")

tk.Label(root, text="Financial Input / Formula:", font=("Arial", 10)).pack(pady=10)
entry = tk.Entry(root, font=("Arial", 14), justify='center')
entry.pack(pady=5, padx=20, fill='x')

# Execution Button
tk.Button(root, text="Calculate (Enter)", command=calculate, height=2, width=35, bg="#E0E0E0").pack(pady=10)

# 1. Memory Row (NEW)
tk.Label(root, text="Memory Functions:", font=("Arial", 9, "bold")).pack()
mem_frame = tk.Frame(root); mem_frame.pack(pady=5)
for i, m_op in enumerate(["M+", "M-", "MR", "MC"]):
    tk.Button(mem_frame, text=m_op, command=lambda o=m_op: memory_op(o), width=9, height=2, bg="#607D8B", fg="white").grid(row=0, column=i, padx=2)

# 2. Finance Row (TVM & Powers)
tk.Label(root, text="Finance Ops (TVM):", font=("Arial", 9, "bold")).pack()
fin_frame = tk.Frame(root); fin_frame.pack(pady=5)
tk.Button(fin_frame, text="x^y", command=lambda: entry.insert(tk.END, "^"), width=9, height=2, bg="#FF9800").grid(row=0, column=0, padx=2)
tk.Button(fin_frame, text="√", command=lambda: finance_op("sqrt"), width=9, height=2, bg="#FF9800").grid(row=0, column=1, padx=2)
tk.Button(fin_frame, text="x²", command=lambda: finance_op("sq"), width=9, height=2, bg="#FF9800").grid(row=0, column=2, padx=2)
tk.Button(fin_frame, text="1/x", command=lambda: entry.insert(0, "1/(")+entry.insert(tk.END, ")"), width=9, height=2, bg="#FF9800").grid(row=0, column=3, padx=2)

# 3. GST Sections
tk.Label(root, text="GST Forward (F1-F4) & Reverse (Alt+F1-F4):", font=("Arial", 9, "bold")).pack(pady=5)
f_frame = tk.Frame(root); f_frame.pack()
r_frame = tk.Frame(root); r_frame.pack(pady=5)
rates = [5, 12, 18, 28]
for i, rate in enumerate(rates):
    tk.Button(f_frame, text=f"{rate}%", command=lambda r=rate: apply_gst(r), bg="#4CAF50", fg="white", width=9, height=2).grid(row=0, column=i, padx=2)
    tk.Button(r_frame, text=f"Rev {rate}%", command=lambda r=rate: apply_gst(r, True), bg="#9C27B0", fg="white", width=9, height=2).grid(row=0, column=i, padx=2)

tk.Button(root, text="Clear Screen (Esc)", command=clear_screen, bg="#f44336", fg="white", height=2, width=35).pack(pady=15)
label_res = tk.Label(root, text="Result: ", font=("Arial", 12, "bold"), fg="#1565C0")
label_res.pack(pady=10)

# Keyboard Shortcuts
entry.focus_force()
root.bind('<Return>', calculate)
root.bind('<KP_Enter>', calculate)
root.bind('<Escape>', clear_screen)
for i, r in enumerate(rates):
    root.bind(f'<F{i+1}>', lambda e, rate=r: apply_gst(rate))
    root.bind(f'<Alt-F{i+1}>', lambda e, rate=r: apply_gst(rate, True))

root.mainloop()