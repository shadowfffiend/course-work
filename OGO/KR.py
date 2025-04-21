import tkinter as tk
from tkinter import messagebox, ttk
import json
import os


class Task:
    """Класс для представления отдельной задачи"""

    def __init__(self, title, description="", due_date="", priority="Средний", completed=False):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = completed

    def toggle_complete(self):
        """Переключает статус выполнения задачи"""
        self.completed = not self.completed

    def to_dict(self):
        """Преобразует задачу в словарь для сохранения"""
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data):
        """Создает задачу из словаря"""
        return cls(
            data["title"],
            data.get("description", ""),
            data.get("due_date", ""),
            data.get("priority", "Средний"),
            data.get("completed", False)
        )


class ToDoList:
    """Класс для управления списком задач"""

    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, task):
        """Добавляет новую задачу"""
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, index):
        """Удаляет задачу по индексу"""
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def toggle_task(self, index):
        """Переключает статус выполнения задачи по индексу"""
        if 0 <= index < len(self.tasks):
            self.tasks[index].toggle_complete()
            self.save_tasks()

    def get_tasks(self, filter_type="Все"):
        """Возвращает задачи с возможностью фильтрации"""
        if filter_type == "Все":
            return self.tasks
        elif filter_type == "Выполненные":
            return [task for task in self.tasks if task.completed]
        elif filter_type == "Невыполненные":
            return [task for task in self.tasks if not task.completed]
        else:  # Фильтрация по приоритету
            return [task for task in self.tasks if task.priority == filter_type]

    def save_tasks(self):
        """Сохраняет задачи в файл JSON"""
        data = [task.to_dict() for task in self.tasks]
        with open("../../tasks.json", "w") as f:
            json.dump(data, f, indent=2)

    def load_tasks(self):
        """Загружает задачи из файла JSON"""
        if os.path.exists("../../tasks.json"):
            try:
                with open("../../tasks.json", "r") as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
            except (json.JSONDecodeError, FileNotFoundError):
                self.tasks = []


class ToDoApp:
    """Главный класс приложения с графическим интерфейсом"""

    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("800x600")

        # Инициализация модели
        self.todo_list = ToDoList()

        # Создание интерфейса
        self.create_widgets()
        self.update_task_list()

    def create_widgets(self):
        """Создает все элементы интерфейса"""
        # Стили
        style = ttk.Style()
        style.configure("Treeview", rowheight=30)

        # Фрейм для добавления новых задач
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill=tk.X)

        ttk.Label(input_frame, text="Новая задача:").grid(row=0, column=0, sticky=tk.W)
        self.task_entry = ttk.Entry(input_frame, width=40)
        self.task_entry.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Описание:").grid(row=1, column=0, sticky=tk.W)
        self.desc_entry = ttk.Entry(input_frame, width=40)
        self.desc_entry.grid(row=1, column=1, padx=5)

        ttk.Label(input_frame, text="Срок выполнения:").grid(row=2, column=0, sticky=tk.W)
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.grid(row=2, column=1, sticky=tk.W, padx=5)

        ttk.Label(input_frame, text="Приоритет:").grid(row=2, column=1, sticky=tk.E, padx=(0, 5))
        self.priority_var = tk.StringVar(value="Средний")
        self.priority_menu = ttk.Combobox(
            input_frame,
            textvariable=self.priority_var,
            values=["Низкий", "Средний", "Высокий"],
            width=10
        )
        self.priority_menu.grid(row=2, column=2, sticky=tk.W)

        add_button = ttk.Button(input_frame, text="Добавить", command=self.add_task)
        add_button.grid(row=3, column=1, pady=10, sticky=tk.E)

        # Фрейм для управления списком
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)

        ttk.Label(control_frame, text="Фильтр:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="Все")
        filter_menu = ttk.Combobox(
            control_frame,
            textvariable=self.filter_var,
            values=["Все", "Выполненные", "Невыполненные", "Низкий", "Средний", "Высокий"],
            width=12,
            state="readonly"
        )
        filter_menu.pack(side=tk.LEFT, padx=5)
        filter_menu.bind("<<ComboboxSelected>>", lambda e: self.update_task_list())

        # Таблица задач
        self.task_tree = ttk.Treeview(
            self.root,
            columns=("title", "description", "due_date", "priority", "status"),
            show="headings",
            selectmode="browse"
        )

        self.task_tree.heading("title", text="Задача")
        self.task_tree.heading("description", text="Описание")
        self.task_tree.heading("due_date", text="Срок")
        self.task_tree.heading("priority", text="Приоритет")
        self.task_tree.heading("status", text="Статус")

        self.task_tree.column("title", width=200)
        self.task_tree.column("description", width=250)
        self.task_tree.column("due_date", width=100)
        self.task_tree.column("priority", width=100)
        self.task_tree.column("status", width=100)

        self.task_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Кнопки управления
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X)

        self.toggle_button = ttk.Button(
            button_frame,
            text="Отметить как выполненное",
            command=self.toggle_task,
            state=tk.DISABLED
        )
        self.toggle_button.pack(side=tk.LEFT, padx=5)

        delete_button = ttk.Button(
            button_frame,
            text="Удалить",
            command=self.delete_task,
            state=tk.DISABLED
        )
        delete_button.pack(side=tk.LEFT, padx=5)

        # Привязка событий
        self.task_tree.bind("<<TreeviewSelect>>", self.on_task_select)

    def add_task(self):
        """Добавляет новую задачу"""
        title = self.task_entry.get().strip()
        if not title:
            messagebox.showwarning("Предупреждение", "Введите название задачи")
            return

        task = Task(
            title=title,
            description=self.desc_entry.get().strip(),
            due_date=self.date_entry.get().strip(),
            priority=self.priority_var.get()
        )

        self.todo_list.add_task(task)
        self.update_task_list()

        # Очистка полей ввода
        self.task_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.priority_var.set("Средний")

    def delete_task(self):
        """Удаляет выбранную задачу"""
        selected_item = self.task_tree.focus()
        if not selected_item:
            return

        index = int(self.task_tree.item(selected_item)["tags"][0])
        self.todo_list.remove_task(index)
        self.update_task_list()

    def toggle_task(self):
        """Изменяет статус выполнения задачи"""
        selected_item = self.task_tree.focus()
        if not selected_item:
            return

        index = int(self.task_tree.item(selected_item)["tags"][0])
        self.todo_list.toggle_task(index)
        self.update_task_list()

    def on_task_select(self, event):
        """Обрабатывает выбор задачи в списке"""
        selected_item = self.task_tree.focus()
        if selected_item:
            self.toggle_button.config(state=tk.NORMAL)
            self.toggle_button.master.children["!button2"].config(state=tk.NORMAL)

            # Получаем статус задачи для правильного текста кнопки
            index = int(self.task_tree.item(selected_item)["tags"][0])
            task = self.todo_list.get_tasks()[index]
            if task.completed:
                self.toggle_button.config(text="Отметить как невыполненное")
            else:
                self.toggle_button.config(text="Отметить как выполненное")
        else:
            self.toggle_button.config(state=tk.DISABLED)
            self.toggle_button.master.children["!button2"].config(state=tk.DISABLED)

    def update_task_list(self):
        """Обновляет список задач в интерфейсе"""
        # Очищаем текущий список
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        # Получаем задачи с учетом фильтра
        tasks = self.todo_list.get_tasks(self.filter_var.get())

        # Добавляем задачи в список
        for i, task in enumerate(tasks):
            status = "Выполнена" if task.completed else "Не выполнена"
            tags = (i,)  # Сохраняем индекс задачи в тегах

            # Изменяем цвет для выполненных задач
            if task.completed:
                self.task_tree.insert(
                    "", tk.END,
                    values=(task.title, task.description, task.due_date, task.priority, status),
                    tags=tags,
                    text="",
                )
                self.task_tree.item(self.task_tree.get_children()[-1], tags=tags)
            else:
                self.task_tree.insert(
                    "", tk.END,
                    values=(task.title, task.description, task.due_date, task.priority, status),
                    tags=tags,
                    text="",
                )


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()