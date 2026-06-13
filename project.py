import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database Connection
conn = sqlite3.connect("employees.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
    emp_id TEXT PRIMARY KEY,
    name TEXT,
    age INTEGER,
    department TEXT,
    salary REAL
)
""")
conn.commit()

# Functions
def add_employee():
    try:
        cursor.execute(
            "INSERT INTO employees VALUES (?, ?, ?, ?, ?)",
            (
                emp_id_var.get(),
                name_var.get(),
                age_var.get(),
                dept_var.get(),
                salary_var.get()
            )
        )
        conn.commit()
        messagebox.showinfo("Success", "Employee Added Successfully")
        clear_fields()
        show_employees()

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Employee ID already exists")

def show_employees():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

def search_employee():
    emp_id = emp_id_var.get()

    cursor.execute(
        "SELECT * FROM employees WHERE emp_id=?",
        (emp_id,)
    )

    row = cursor.fetchone()

    if row:
        name_var.set(row[1])
        age_var.set(row[2])
        dept_var.set(row[3])
        salary_var.set(row[4])
    else:
        messagebox.showerror("Error", "Employee Not Found")

def update_employee():
    cursor.execute("""
    UPDATE employees
    SET name=?, age=?, department=?, salary=?
    WHERE emp_id=?
    """,
    (
        name_var.get(),
        age_var.get(),
        dept_var.get(),
        salary_var.get(),
        emp_id_var.get()
    ))

    conn.commit()
    messagebox.showinfo("Success", "Employee Updated")
    show_employees()

def delete_employee():
    cursor.execute(
        "DELETE FROM employees WHERE emp_id=?",
        (emp_id_var.get(),)
    )

    conn.commit()
    messagebox.showinfo("Success", "Employee Deleted")
    clear_fields()
    show_employees()

def clear_fields():
    emp_id_var.set("")
    name_var.set("")
    age_var.set("")
    dept_var.set("")
    salary_var.set("")

# GUI Window
root = tk.Tk()
root.title("Employee Management System")
root.geometry("900x550")

# Variables
emp_id_var = tk.StringVar()
name_var = tk.StringVar()
age_var = tk.StringVar()
dept_var = tk.StringVar()
salary_var = tk.StringVar()

# Labels & Entries
tk.Label(root, text="Employee ID").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=emp_id_var).grid(row=0, column=1)

tk.Label(root, text="Name").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=name_var).grid(row=1, column=1)

tk.Label(root, text="Age").grid(row=2, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=age_var).grid(row=2, column=1)

tk.Label(root, text="Department").grid(row=3, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=dept_var).grid(row=3, column=1)

tk.Label(root, text="Salary").grid(row=4, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=salary_var).grid(row=4, column=1)

# Buttons
tk.Button(root, text="Add", width=15,
          command=add_employee).grid(row=5, column=0, pady=10)

tk.Button(root, text="Search", width=15,
          command=search_employee).grid(row=5, column=1)

tk.Button(root, text="Update", width=15,
          command=update_employee).grid(row=6, column=0)

tk.Button(root, text="Delete", width=15,
          command=delete_employee).grid(row=6, column=1)

tk.Button(root, text="Clear", width=15,
          command=clear_fields).grid(row=7, column=0, columnspan=2, pady=10)

# Table
columns = ("ID", "Name", "Age", "Department", "Salary")

tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.grid(row=0, column=3, rowspan=10, padx=20, pady=20)

show_employees()

root.mainloop()

conn.close()