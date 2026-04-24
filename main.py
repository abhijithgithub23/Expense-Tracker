import tkinter as tk
from tkinter import ttk, messagebox
import data  # Imports our CRUD logic

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("700x650") # Slightly taller to comfortably fit the new layout
        
        # --- TOP SECTION: Input Fields ---
        input_frame = tk.Frame(self.root, pady=10)
        input_frame.pack(fill=tk.X)

        tk.Label(input_frame, text="Amount (₹):").grid(row=0, column=0, padx=5)
        self.amount_var = tk.StringVar()
        tk.Entry(input_frame, textvariable=self.amount_var, width=15).grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Type:").grid(row=0, column=2, padx=5)
        self.type_var = tk.StringVar(value="Expense")
        type_dropdown = ttk.Combobox(input_frame, textvariable=self.type_var, values=["Income", "Expense"], state="readonly", width=10)
        type_dropdown.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Category:").grid(row=0, column=4, padx=5)
        self.category_var = tk.StringVar()
        categories = ["Food", "Travel", "Bills", "Salary", "Entertainment", "Other"]
        cat_dropdown = ttk.Combobox(input_frame, textvariable=self.category_var, values=categories, width=12)
        cat_dropdown.grid(row=0, column=5, padx=5)

        tk.Button(input_frame, text="Add Transaction", command=self.add_entry, bg="green", fg="white").grid(row=0, column=6, padx=10)

        # --- MIDDLE SECTION: Table (Treeview) ---
        table_frame = tk.Frame(self.root, pady=10)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Amount", "Type", "Category", "Date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20)

        # --- ACTIONS SECTION: Update & Delete Buttons ---
        action_frame = tk.Frame(self.root, pady=5)
        action_frame.pack(fill=tk.X, padx=15)
        
        tk.Button(action_frame, text="Update Selected", command=self.update_entry, bg="orange").pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Delete Selected", command=self.delete_entry, bg="red", fg="white").pack(side=tk.LEFT, padx=5)

        # --- DASHBOARD SECTION: Balances & Summaries ---
        dashboard_frame = tk.Frame(self.root, pady=15)
        dashboard_frame.pack(fill=tk.BOTH, padx=20)

        self.balance_label = tk.Label(dashboard_frame, text="Balance: ₹0.00", font=("Arial", 13, "bold"))
        self.balance_label.pack(anchor="w") # anchor="w" aligns the text to the left (West)

        # wraplength ensures long category lists drop to the next line instead of getting cut off
        self.summary_label = tk.Label(dashboard_frame, text="", font=("Arial", 11), justify=tk.LEFT, wraplength=650)
        self.summary_label.pack(anchor="w", pady=8)

        # Bind row selection to populate entry fields for easy updating
        self.tree.bind('<ButtonRelease-1>', self.select_item)

        # Initial Load
        self.refresh_ui()

    def refresh_ui(self):
        """Clears the table and reloads data from the JSON file."""
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        records = data.load_data()
        for record in records:
            self.tree.insert("", tk.END, values=(record["id"], f"₹{record['amount']}", record["type"], record["category"], record["date"]))
            
        self.update_dashboard()

    def update_dashboard(self):
        """Updates the balance and category summary."""
        income, expense, balance = data.get_balance()
        self.balance_label.config(text=f"Total Income: ₹{income}   |   Expenses: ₹{expense}   |   Net Balance: ₹{balance}")
        
        summary = data.get_category_summary()
        if summary:
            summary_text = "Expense Breakdown:\n" + "  •  ".join([f"{k}: ₹{v}" for k, v in summary.items()])
        else:
            summary_text = "Expense Breakdown: No expenses yet."
            
        self.summary_label.config(text=summary_text)

    def add_entry(self):
        amount = self.amount_var.get()
        trans_type = self.type_var.get()
        category = self.category_var.get()

        if not amount or not category:
            messagebox.showerror("Error", "Amount and Category are required!")
            return
        try:
            float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")
            return

        data.add_transaction(amount, trans_type, category)
        self.amount_var.set("")
        self.category_var.set("")
        self.refresh_ui()

    def select_item(self, event):
        """Populates the input fields when a row is clicked."""
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, 'values')
        
        # values[1] has the ₹ symbol, we need to strip it out
        clean_amount = values[1].replace('₹', '')
        
        self.amount_var.set(clean_amount)
        self.type_var.set(values[2])
        self.category_var.set(values[3])

    def update_entry(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a row to update.")
            return
            
        trans_id = int(self.tree.item(selected, 'values')[0])
        amount = self.amount_var.get()
        trans_type = self.type_var.get()
        category = self.category_var.get()
        
        try:
            float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")
            return

        data.update_transaction(trans_id, amount, trans_type, category)
        self.amount_var.set("")
        self.category_var.set("")
        self.refresh_ui()

    def delete_entry(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a row to delete.")
            return
            
        trans_id = int(self.tree.item(selected, 'values')[0])
        data.delete_transaction(trans_id)
        self.amount_var.set("")
        self.category_var.set("")
        self.refresh_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()