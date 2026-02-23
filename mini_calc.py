import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import os
import math

# Logging function for professional records
def save_entry(action, result):
    file_path = os.path.expanduser('~/python_projects/tax_log.csv')
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), action, result])

def calculate(event=None):
    try:
        val = entry.get()
        if not val: return
        # Replaces '^' with '**' for easy power calculations like (1+r)^n
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
            tax = val - base
            label_res.config(text=f"Base: {base:.2f} | {rate}% GST: {tax:.2f}")
        else:
            tax = val * (rate/100)
            total = val + tax
            label_res.config(text=f"GST: {tax:.2f} | Total: {total:.2f}")
    except:
        messagebox.showerror("Error", "Enter a numeric value")

def finance_op(op):
    try:
        val = float(entry.get())
        if op == "sqrt": res = math.sqrt(val)
        if op == "sq": res = val ** 2
        label_res.config(text=f"Result: {res}")
    except:
        messagebox.showerror("Error", "Enter a number first")

def clear_screen(event=None):
    entry.delete(0, tk.END)
    label_res.config(text="Result: ")

# GUI Setup
root = tk.Tk()
root.title("CA Finalist Pro Financial Calc")
root.geometry("450x650")

tk.Label(root, text="Financial Input / Formula:", font=("Arial", 10)).pack(pady=10)
entry = tk.Entry(root, font=("Arial", 14), justify='center')
entry.pack(pady=5, padx=20, fill='x')

# Standard Calculation
tk.Button(root, text="Calculate (Enter)", command=calculate, height=2, width=30, bg="#E0E0E0", takefocus=0).pack(pady=10)

# --- NEW FINANCE ROW ---
tk.Label(root, text="Finance Ops:", font=("Arial", 9, "bold")).pack()
fin_frame = tk.Frame(root)
fin_frame.pack(pady=5)

# Power button is essential for TVM formulas like (1+i)^n
tk.Button(fin_frame, text="x^y", command=lambda: entry.insert(tk.END, "^"), width=8, height=2, bg="#FF9800").grid(row=0, column=0, padx=2)
tk.Button(fin_frame, text="√", command=lambda: finance_op("sqrt"), width=8, height=2, bg="#FF9800").grid(row=0, column=1, padx=2)
tk.Button(fin_frame, text="x²", command=lambda: finance_op("sq"), width=8, height=2, bg="#FF9800").grid(row=0, column=2, padx=2)
tk.Button(fin_frame, text="1/x", command=lambda: entry.insert(0, "1/(")+entry.insert(tk.END, ")"), width=8, height=2, bg="#FF9800").grid(row=0, column=3, padx=2)

# GST Sections (Forward & Reverse)
tk.Label(root, text="Forward GST (F1-F4) | Reverse GST (Alt+F1-F4)", font=("Arial", 9, "bold")).pack(pady=5)
f_frame = tk.Frame(root); f_frame.pack()
r_frame = tk.Frame(root); r_frame.pack(pady=5)
rates = [5, 12, 18, 28]

for i, rate in enumerate(rates):
    tk.Button(f_frame, text=f"{rate}%", command=lambda r=rate: apply_gst(r), bg="#4CAF50", fg="white", width=8, height=2).grid(row=0, column=i, padx=2)
    tk.Button(r_frame, text=f"Rev {rate}%", command=lambda r=rate: apply_gst(r, True), bg="#9C27B0", fg="white", width=8, height=2).grid(row=0, column=i, padx=2)

tk.Button(root, text="Clear Screen (Esc)", command=clear_screen, bg="#f44336", fg="white", height=2, width=30).pack(pady=15)
label_res = tk.Label(root, text="Result: ", font=("Arial", 12, "bold"), fg="#1565C0")
label_res.pack(pady=10)

# Keyboard Bindings
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