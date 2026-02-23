import pandas as pd
import os

def run_reconciliation():
    path = os.path.expanduser('~/python_projects/')
    bank = pd.read_csv(path + 'bank_statement.csv')
    cash = pd.read_csv(path + 'cash_book.csv')

    # Find discrepancies
    not_in_cash = bank[~bank['Amount'].isin(cash['Amount'])]
    not_in_bank = cash[~cash['Amount'].isin(bank['Amount'])]

    # Save to a professional report for audit evidence
    with pd.ExcelWriter(path + 'BRS_Exception_Report.xlsx') as writer:
        not_in_cash.to_excel(writer, sheet_name='Missing_in_CashBook', index=False)
        not_in_bank.to_excel(writer, sheet_name='Unpresented_Items', index=False)
    
    print("--- Reconciliation Complete ---")
    print(f"Report saved to: {path}BRS_Exception_Report.xlsx")

if __name__ == "__main__":
    run_reconciliation()