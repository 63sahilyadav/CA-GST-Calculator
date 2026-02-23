import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

def select_file(entry_field):
    filename = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
    if filename:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, filename)

def run_reconciliation():
    bank_path = entry_bank.get()
    cash_path = entry_cash.get()
    
    if not bank_path or not cash_path:
        messagebox.showwarning("Input Error", "Please select both Bank and Cash Book files.")
        return

    try:
        # Load the data
        bank = pd.read_csv(bank_path)
        cash = pd.read_csv(cash_path)

        # Reconciliation Logic: Finding mismatches based on 'Amount'
        not_in_cash = bank[~bank['Amount'].isin(cash['Amount'])]
        not_in_bank = cash[~cash['Amount'].isin(bank['Amount'])]

        # Save to a professional Excel report
        output_path = os.path.expanduser('~/python_projects/BRS_Final_Report.xlsx')
        with pd.ExcelWriter(output_path) as writer:
            not_in_cash.to_excel(writer, sheet_name='Missing_in_CashBook', index=False)
            not_in_bank.to_excel(writer, sheet_name='Unpresented_Items', index=False)
        
        messagebox.showinfo("Success", f"Reconciliation Complete!\nReport saved to: {output_path}")
    except Exception as e:
        messagebox.showerror("Technical Error", f"Could not process files: {str(e)}")

# UI Setup
root = tk.Tk()
root.title("CA Pro: Bank Reconciliation Tool")
root.geometry("500x350")

tk.Label(root, text="Bank Reconciliation Automation", font=("Arial", 12, "bold")).pack(pady=10)

# Bank File Selection
tk.Label(root, text="Select Bank Statement (CSV):").pack()
frame_bank = tk.Frame(root); frame_bank.pack(pady=5)
entry_bank = tk.Entry(frame_bank, width=40)
entry_bank.pack(side=tk.LEFT, padx=5)
tk.Button(frame_bank, text="Browse", command=lambda: select_file(entry_bank)).pack(side=tk.LEFT)

# Cash Book Selection
tk.Label(root, text="Select Cash Book (CSV):").pack()
frame_cash = tk.Frame(root); frame_cash.pack(pady=5)
entry_cash = tk.Entry(frame_cash, width=40)
entry_cash.pack(side=tk.LEFT, padx=5)
tk.Button(frame_cash, text="Browse", command=lambda: select_file(entry_cash)).pack(side=tk.LEFT)

# Execute Button
tk.Button(root, text="Generate Exception Report", command=run_reconciliation, 
          bg="#2E7D32", fg="white", height=2, width=30).pack(pady=30)

root.mainloop()