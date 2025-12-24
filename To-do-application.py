import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

FILE_NAME = "tasks.txt"

root = tk.Tk()
root.title("To-Do Application")
root.geometry("550x580")
root.config(bg="#f4f6f8")

def add_task(event=None):
    task = task_entry.get().strip()
    if task == "":
        messagebox.showwarning("Warning", "Enter a task")
        return

    today = datetime.now().strftime("%a, %d %b")
    tree.insert("", tk.END, values=("☐", task, today))
    task_entry.delete(0, tk.END)
    save_tasks()

def toggle_task(event):
    region = tree.identify("region", event.x, event.y)
    column = tree.identify_column(event.x)

    if region != "cell" or column != "#1":
        return

    selected = tree.focus()
    if not selected:
        return

    status, task, date = tree.item(selected, "values")
    new_status = "☑" if status == "☐" else "☐"
    tree.item(selected, values=(new_status, task, date))
    save_tasks()

def delete_task():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select a task")
        return
    tree.delete(selected)
    save_tasks()

def clear_tasks():
    if messagebox.askyesno("Confirm", "Clear all tasks?"):
        for item in tree.get_children():
            tree.delete(item)
        save_tasks()

def save_tasks():
    with open(FILE_NAME, "w") as file:
        for item in tree.get_children():
            values = tree.item(item, "values")
            file.write("|".join(values) + "\n")

def load_tasks():
    if not os.path.exists(FILE_NAME):
        return
    with open(FILE_NAME, "r") as file:
        for line in file:
            parts = line.strip().split("|")
            if len(parts) == 3:
                tree.insert("", tk.END, values=parts)

menu_bar = tk.Menu(root)
task_menu = tk.Menu(menu_bar, tearoff=0)
task_menu.add_command(label="Add Task", command=add_task)
task_menu.add_command(label="Delete Task", command=delete_task)
task_menu.add_command(label="Clear All", command=clear_tasks)
task_menu.add_separator()
task_menu.add_command(label="Exit", command=root.quit)

menu_bar.add_cascade(label="Options", menu=task_menu)
root.config(menu=menu_bar)

title = tk.Label(
    root, text="📝 Smart To-Do List",
    font=("Segoe UI", 20, "bold"),
    bg="#f4f6f8"
)
title.pack(pady=15)

task_entry = tk.Entry(root, font=("Segoe UI", 14), relief=tk.FLAT)
task_entry.pack(padx=25, pady=10, fill=tk.X)
task_entry.bind("<Return>", add_task)

columns = ("Status", "Task", "Date")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

tree.heading("Status", text="Done")
tree.heading("Task", text="Task")
tree.heading("Date", text="Day & Date")

tree.column("Status", width=60, anchor="center")
tree.column("Task", width=280)
tree.column("Date", width=120, anchor="center")

tree.pack(padx=25, pady=10, fill=tk.BOTH, expand=True)
tree.bind("<ButtonRelease-1>", toggle_task)

btn_frame = tk.Frame(root, bg="#f4f6f8")
btn_frame.pack(pady=15)

ttk.Button(btn_frame, text="Add", command=add_task).grid(row=0, column=0, padx=10)
ttk.Button(btn_frame, text="Delete", command=delete_task).grid(row=0, column=1, padx=10)
ttk.Button(btn_frame, text="Clear", command=clear_tasks).grid(row=0, column=2, padx=10)

load_tasks()
root.mainloop()
