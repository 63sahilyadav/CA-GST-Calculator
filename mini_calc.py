import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import os

# Function to log your work for professional records
def save_entry(action, result):
    file_path = os.path.expanduser('~/python_projects/tax_log.csv')
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), action, result])

def calculate(event=None):
    try:
        val = entry.get()
        if not val: return
        res = eval(val)
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
            save_entry(f"Reverse {rate}% on {val}", base)
        else:
            tax = val * (rate/100)
            total = val + tax
            label_res.config(text=f"GST: {tax:.2f} | Total: {total:.2f}")
            save_entry(f"Forward {rate}% on {val}", total)
    except:
        messagebox.showerror("Error", "Enter a numeric value")

def clear_screen(event=None):
    entry.delete(0, tk.END)
    label_res.config(text="Result: ")

# GUI Setup
root = tk.Tk()
root.title("CA Final Pro-Speed Calc")
root.geometry("450x600")

tk.Label(root, text="Enter Amount/Calculation:", font=("Arial", 10)).pack(pady=10)
entry = tk.Entry(root, font=("Arial", 14), justify='center')
entry.pack(pady=5, padx=20, fill='x')

# Standard Calculation Button
tk.Button(root, text="Calculate (Enter)", command=calculate, height=2, width=30, takefocus=0).pack(pady=15)

# GST Help Text for Shortcuts
tk.Label(root, text="Forward GST (F1-F4) | Reverse GST (Alt+F1-F4)", font=("Arial", 9, "bold")).pack(pady=5)

# Forward GST Buttons
f_frame = tk.Frame(root)
f_frame.pack()
rates = [5, 12, 18, 28]
for i, rate in enumerate(rates):
    tk.Button(f_frame, text=f"{rate}%", command=lambda r=rate: apply_gst(r), 
              bg="#4CAF50", fg="white", width=8, height=2, takefocus=0).grid(row=0, column=i, padx=3)

# Reverse GST Buttons
r_frame = tk.Frame(root)
r_frame.pack(pady=10)
for i, rate in enumerate(rates):
    tk.Button(r_frame, text=f"Rev {rate}%", command=lambda r=rate: apply_gst(r, True), 
              bg="#9C27B0", fg="white", width=8, height=2, takefocus=0).grid(row=0, column=i, padx=3)

tk.Button(root, text="Clear Screen (Esc)", command=clear_screen, bg="#f44336", fg="white", height=2, width=30, takefocus=0).pack(pady=20)

label_res = tk.Label(root, text="Result: ", font=("Arial", 12, "bold"), fg="#1565C0")
label_res.pack(pady=10)

# --- KEYBOARD FIXES & SHORTCUTS ---
entry.focus_force() 
root.bind('<Return>', calculate)   
root.bind('<KP_Enter>', calculate) 
root.bind('<Escape>', clear_screen) 

# GST Forward Shortcuts
root.bind('<F1>', lambda e: apply_gst(5))
root.bind('<F2>', lambda e: apply_gst(12))
root.bind('<F3>', lambda e: apply_gst(18))
root.bind('<F4>', lambda e: apply_gst(28))

# GST Reverse Shortcuts
root.bind('<Alt-F1>', lambda e: apply_gst(5, True))
root.bind('<Alt-F2>', lambda e: apply_gst(12, True))
root.bind('<Alt-F3>', lambda e: apply_gst(18, True))
root.bind('<Alt-F4>', lambda e: apply_gst(28, True))

root.mainloop()
