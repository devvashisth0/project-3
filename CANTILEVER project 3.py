import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Setting up the database
conn = sqlite3.connect('finance.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS transactions
             (id INTEGER PRIMARY KEY, date TEXT, type TEXT, category TEXT, amount REAL)''')
conn.commit()

# Main Application Window
root = tk.Tk()
root.title("Personal Finance Management System")
root.geometry("900x600")

# Function to add a transaction
def add_transaction():
    date = entry_date.get()
    t_type = entry_type.get()
    category = entry_category.get()
    amount = entry_amount.get()
    
    c.execute("INSERT INTO transactions (date, type, category, amount) VALUES (?, ?, ?, ?)",
              (date, t_type, category, amount))
    conn.commit()
    update_treeview()

# Function to update the Treeview
def update_treeview():
    for i in tree.get_children():
        tree.delete(i)
    c.execute("SELECT * FROM transactions")
    rows = c.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

# Function to create charts
def create_charts():
    c.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Income' GROUP BY category")
    income_data = c.fetchall()

    c.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Expense' GROUP BY category")
    expense_data = c.fetchall()

    categories = [x[0] for x in income_data]
    income_values = [x[1] for x in income_data]

    categories_exp = [x[0] for x in expense_data]
    expense_values = [x[1] for x in expense_data]

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].bar(categories, income_values, color='green')
    ax[0].set_title('Income by Category')
    ax[1].bar(categories_exp, expense_values, color='red')
    ax[1].set_title('Expense by Category')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=5, column=0, columnspan=4)

# Creating the input fields and labels
label_date = tk.Label(root, text="Date (YYYY-MM-DD):")
label_date.grid(row=0, column=0)
entry_date = tk.Entry(root)
entry_date.grid(row=0, column=1)

label_type = tk.Label(root, text="Type (Income/Expense):")
label_type.grid(row=1, column=0)
entry_type = tk.Entry(root)
entry_type.grid(row=1, column=1)

label_category = tk.Label(root, text="Category:")
label_category.grid(row=2, column=0)
entry_category = tk.Entry(root)
entry_category.grid(row=2, column=1)

label_amount = tk.Label(root, text="Amount:")
label_amount.grid(row=3, column=0)
entry_amount = tk.Entry(root)
entry_amount.grid(row=3, column=1)

# Adding the buttons
btn_add = tk.Button(root, text="Add Transaction", command=add_transaction)
btn_add.grid(row=4, column=0, columnspan=2)

btn_chart = tk.Button(root, text="Show Charts", command=create_charts)
btn_chart.grid(row=4, column=2, columnspan=2)

# Creating the Treeview to display transactions
columns = ("ID", "Date", "Type", "Category", "Amount")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("ID", text="ID")
tree.heading("Date", text="Date")
tree.heading("Type", text="Type")
tree.heading("Category", text="Category")
tree.heading("Amount", text="Amount")

tree.grid(row=5, column=0, columnspan=4)

# Initial population of the Treeview
update_treeview()

root.mainloop()

# Closing the database connection
conn.close()
