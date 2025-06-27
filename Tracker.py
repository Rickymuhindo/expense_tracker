import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import os
import matplotlib.pyplot as plt

expenses = []
budget = 0.0
expense_file = r'C:\Users\Ricky\Downloads\expense.txt'

# Load previous expenses
def load_expenses():
    if os.path.exists(expense_file):
        with open(expense_file, "r") as file:
            for line in file:
                try:
                    amount, category, description, date_str = line.strip().split(",")
                    expenses.append({
                        "amount": float(amount),
                        "category": category,
                        "description": description,
                        "date": date_str
                    })
                except ValueError:
                    continue

# Save expenses
def save_expenses():
    with open(expense_file, "w") as file:
        for expense in expenses:
            file.write(f"{expense['amount']},{expense['category']},{expense['description']},{expense['date']}\n")
    messagebox.showinfo("Save", "Expenses saved successfully!")

# Add expense
def add_expense():
    try:
        amount = float(amount_entry.get())
        category = category_entry.get()
        description = description_entry.get()
        date = date_entry.get()
        if not date:
            date = datetime.today().strftime('%Y-%m-%d')
        expenses.append({
            "amount": amount,
            "category": category,
            "description": description,
            "date": date
        })
        messagebox.showinfo("Success", "Expense added successfully.")
        clear_entries()
        update_expense_list()
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")

def clear_entries():
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)

def update_expense_list():
    expense_listbox.delete(0, tk.END)
    for i, expense in enumerate(expenses, 1):
        item = f"{i}. ${expense['amount']:.2f} | {expense['category']} | {expense['description']} | {expense['date']}"
        expense_listbox.insert(tk.END, item)

def show_summary():
    summary = {}
    for expense in expenses:
        category = expense['category']
        summary[category] = summary.get(category, 0) + expense['amount']

    if not summary:
        messagebox.showinfo("Expense Summary", "No expenses to summarize.")
        return

    categories = list(summary.keys())
    amounts = list(summary.values())

    # Pie chart version
    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Expense Summary by Category")
    plt.tight_layout()
    plt.show()

def set_budget():
    global budget
    try:
        budget_input = simpledialog.askfloat("Set Budget", "Enter your monthly budget:")
        if budget_input is not None:
            budget = budget_input
            messagebox.showinfo("Budget", f"Budget set to ${budget:.2f}")
    except Exception:
        messagebox.showerror("Error", "Invalid input.")

def view_remaining_budget():
    if budget == 0:
        messagebox.showinfo("Budget", "Please set a budget first.")
        return
    total_spent = sum(expense['amount'] for expense in expenses)
    remaining = budget - total_spent
    messagebox.showinfo("Remaining Budget", f"Budget: ${budget:.2f}\nSpent: ${total_spent:.2f}\nRemaining: ${remaining:.2f}")

# GUI setup
load_expenses()

root = tk.Tk()
root.title("Expense Tracker")

# Inputs
tk.Label(root, text="Amount ($):").grid(row=0, column=0, sticky="e")
tk.Label(root, text="Category:").grid(row=1, column=0, sticky="e")
tk.Label(root, text="Description:").grid(row=2, column=0, sticky="e")
tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="e")

amount_entry = tk.Entry(root)
category_entry = tk.Entry(root)
description_entry = tk.Entry(root)
date_entry = tk.Entry(root)

amount_entry.grid(row=0, column=1, padx=5, pady=2)
category_entry.grid(row=1, column=1, padx=5, pady=2)
description_entry.grid(row=2, column=1, padx=5, pady=2)
date_entry.grid(row=3, column=1, padx=5, pady=2)

# Buttons
tk.Button(root, text="Add Expense", command=add_expense).grid(row=4, column=0, pady=5)
tk.Button(root, text="Show Summary", command=show_summary).grid(row=4, column=1, pady=5)
tk.Button(root, text="Set Budget", command=set_budget).grid(row=5, column=0, pady=5)
tk.Button(root, text="View Remaining", command=view_remaining_budget).grid(row=5, column=1, pady=5)
tk.Button(root, text="Save & Exit", command=lambda: [save_expenses(), root.destroy()]).grid(row=6, column=0, columnspan=2, pady=10)

# Expense list
expense_listbox = tk.Listbox(root, width=60)
expense_listbox.grid(row=7, column=0, columnspan=2, padx=5, pady=10)

update_expense_list()
root.mainloop()
