import sqlite3

class Database:
    def __init__(self, db_name='tasks.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                category TEXT NOT NULL,
                priority TEXT NOT NULL,
                due_date TEXT,
                completed BOOLEAN DEFAULT FALSE
            )
        ''')
        self.conn.commit()

    def add_task(self, task, category, priority, due_date):
        self.cursor.execute('''
            INSERT INTO tasks (task, category, priority, due_date)
            VALUES (?, ?, ?, ?)
        ''', (task, category, priority, due_date))
        self.conn.commit()

    def remove_task(self, task_id):
        self.cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
        self.conn.commit()

    def mark_completed(self, task_id):
        self.cursor.execute('UPDATE tasks SET completed=TRUE WHERE id=?', (task_id,))
        self.conn.commit()

    def get_tasks(self, sort_by=None, search_query=None, category=None, priority=None):
        query = 'SELECT * FROM tasks'
        params = []

        if search_query:
            query += ' WHERE task LIKE ?'
            params.append(f'%{search_query}%')

        if category:
            query += ' AND category=?' if params else ' WHERE category=?'
            params.append(category)

        if priority:
            query += ' AND priority=?' if params else ' WHERE priority=?'
            params.append(priority)

        if sort_by:
            query += f' ORDER BY {sort_by}'

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.db = Database()

        self.create_widgets()

    def create_widgets(self):
        # Фрейм для добавления задач
        self.add_frame = ttk.Frame(self.root)
        self.add_frame.pack(pady=10)

        ttk.Label(self.add_frame, text="Task:").grid(row=0, column=0, padx=5, pady=5)
        self.task_entry = ttk.Entry(self.add_frame)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.add_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5)
        self.category_var = tk.StringVar(value="Работа")
        ttk.Combobox(self.add_frame, textvariable=self.category_var, values=["Работа", "Дом", "Учеба"]).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.add_frame, text="Priority:").grid(row=2, column=0, padx=5, pady=5)
        self.priority_var = tk.StringVar(value="Средний")
        ttk.Combobox(self.add_frame, textvariable=self.priority_var, values=["Высокий", "Средний", "Низкий"]).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.add_frame, text="Due Date:").grid(row=3, column=0, padx=5, pady=5)
        self.due_date_entry = ttk.Entry(self.add_frame)
        self.due_date_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(self.add_frame, text="Add Task", command=self.add_task).grid(row=4, column=0, columnspan=2, pady=10)

        # Фрейм для управления задачами
        self.manage_frame = ttk.Frame(self.root)
        self.manage_frame.pack(pady=10)

        ttk.Button(self.manage_frame, text="Remove Selected Task", command=self.remove_task).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.manage_frame, text="Mark as Completed", command=self.mark_completed).grid(row=0, column=1, padx=5, pady=5)

        # Фрейм для фильтрации и сортировки
        self.filter_frame = ttk.Frame(self.root)
        self.filter_frame.pack(pady=10)

        ttk.Label(self.filter_frame, text="Sort by:").grid(row=0, column=0, padx=5, pady=5)
        self.sort_var = tk.StringVar(value="due_date")
        ttk.Combobox(self.filter_frame, textvariable=self.sort_var, values=["due_date", "priority"]).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.filter_frame, text="Search:").grid(row=1, column=0, padx=5, pady=5)
        self.search_entry = ttk.Entry(self.filter_frame)
        self.search_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.filter_frame, text="Apply Filters", command=self.update_task_list).grid(row=2, column=0, columnspan=2, pady=10)

        # Таблица для отображения задач
        self.tree = ttk.Treeview(self.root, columns=("ID", "Task", "Category", "Priority", "Due Date", "Completed"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Task", text="Task")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Completed", text="Completed")
        self.tree.pack(pady=10)

        self.update_task_list()

    def add_task(self):
        task = self.task_entry.get()
        category = self.category_var.get()
        priority = self.priority_var.get()
        due_date = self.due_date_entry.get()

        if not task or not category or not priority or not due_date:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Input Error", "Invalid date format! Use YYYY-MM-DD.")
            return

        self.db.add_task(task, category, priority, due_date)
        self.update_task_list()
        self.task_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)

    def remove_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a task to remove!")
            return

        task_id = self.tree.item(selected_item[0])['values'][0]
        self.db.remove_task(task_id)
        self.update_task_list()

    def mark_completed(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed!")
            return

        task_id = self.tree.item(selected_item[0])['values'][0]
        self.db.mark_completed(task_id)
        self.update_task_list()

    def update_task_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        sort_by = self.sort_var.get()
        search_query = self.search_entry.get()

        tasks = self.db.get_tasks(sort_by=sort_by, search_query=search_query)
        for task in tasks:
            self.tree.insert("", tk.END, values=task)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()