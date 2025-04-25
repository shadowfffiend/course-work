from tkinter import *
from tkinter import ttk
from task import TaskManager
from tkcalendar import DateEntry


class ToDoApp():
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.minsize(700,600)
        self.root.maxsize(1000, 1000)
        self.root.title("To Do")

        # Стиль
        self.style = ttk.Style()
        self.style.theme_use('xpnative')

        self.manager = TaskManager()

        # основные фреймы
        self.input_frame = ttk.Frame(self.root, padding=10)
        self.input_frame.pack(fill=BOTH, expand=True)  # Верхняя часть - форма ввода

        self.filter_frame = ttk.Frame(self.root, padding=10)
        self.filter_frame.pack(fill=X, expand=True)  # размещаем фильтр между формой ввода и таблицей

        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(fill=BOTH, expand=True)  # центр - таблица

        self.button_frame = ttk.Frame(self.root, padding=10)
        self.button_frame.pack(fill=BOTH, expand=True)  # низ - кнопки управления

        self.logo_text = Label(
            self.root,
            text="TO DO\n✅APP",
            font=('Arial', 40, 'bold'),
            fg='#333333',  # цвет
            justify=RIGHT,  # выравнивание
            padx=50,
            pady=5
        )
        self.logo_text2 = Label(
            self.root,
            text="DERIN TECH",  # Текст в 3 строки
            font=('Arial', 15, 'bold'),  # Шрифт как на скриншоте
            fg='#333333',  # Цвет текста
            justify=RIGHT,  # Выравнивание по правому краю
            padx=50,  # Отступы
            pady=5
        )
        self.logo_text.place(relx=1.0, rely=0.0, anchor=NE, x=-10, y=10)
        self.logo_text2.place(relx=1.0, rely=0.0, anchor=NE, x=-10, y=150)

        self._create_widgets()
        self._create_tasks_tree()


    def _create_widgets(self):
        """Создаем элементы формы ввода"""
        # Новая задача
        ttk.Label(self.input_frame, text="Новая задача:").grid(row=0, column=0, sticky=W)
        self.entry_task = ttk.Entry(self.input_frame, width=40)
        self.entry_task.grid(row=0, column=1, padx=5, pady=5)

        # Описание
        ttk.Label(self.input_frame, text="Описание:").grid(row=1, column=0, sticky=W)
        self.description = ttk.Entry(self.input_frame, width=40)
        self.description.grid(row=1, column=1, padx=5, pady=5)

        # Приоритет
        ttk.Label(self.input_frame, text="Приоритет:").grid(row=2, column=0, sticky=W)
        self.priority = ttk.Combobox(self.input_frame,
                                     values=["Низкий", "Средний", "Высокий"],
                                     width=15)
        self.priority.grid(row=2, column=1, padx=5, pady=5, sticky=EW)
        self.priority.current(1)  # Значение по умолчанию "Средний"

        # Срок выполнения
        ttk.Label(self.input_frame, text="Срок выполнения:").grid(row=3, column=0, sticky=W)
        self.due_date = DateEntry(self.input_frame,
                                  width=15,
                                  background="gray",
                                  foreground='white',
                                  borderwidth=2,
                                  date_pattern="dd.mm.yyyy",
                                  font=('Arial', 10))
        self.due_date.grid(row=3, column=1, padx=5, pady=5, sticky=EW)

        # Кнопка добавления
        self.add_button = ttk.Button(
            self.input_frame,
            text="Добавить",
            # command=self.add_task
        )
        self.add_button.grid(row=4, column=0, pady=10, sticky=NSEW, columnspan=2)

        # Фильтр
        ttk.Label(self.filter_frame, text="Фильтр:").pack(side=LEFT, padx=5, pady=5)
        self.filter = ttk.Combobox(self.filter_frame,
                                   values=["Все", "Выполненные", "Невыполненные", "Низкий", "Средний", "Высокий"],
                                   width=20,
                                   state="readonly")
        self.filter.pack(side=LEFT, padx=5, pady=5)
        self.filter.current(0)

    def _create_tasks_tree(self):
        """Создаем таблицу задач"""
        self.task_tree = ttk.Treeview(
            self.tree_frame,
            columns=("title", "description", "due_date", "priority", "status"),
            show="headings",
            selectmode="browse"
        )

        # Настраиваем заголовки
        self.task_tree.heading("title", text="Задача")
        self.task_tree.heading("description", text="Описание")
        self.task_tree.heading("due_date", text="Срок")
        self.task_tree.heading("priority", text="Приоритет")
        self.task_tree.heading("status", text="Статус")

        # Настраиваем колонки
        self.task_tree.column("title", width=200)
        self.task_tree.column("description", width=250)
        self.task_tree.column("due_date", width=100)
        self.task_tree.column("priority", width=100)
        self.task_tree.column("status", width=100)

        # Добавляем прокрутку
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)

        # Размещаем таблицу и скроллбар
        self.task_tree.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
        scrollbar.pack(side=RIGHT, fill=Y, ipadx=5)

        # Кнопки управления в нижнем фрейме
        self.done_button = ttk.Button(
            self.button_frame,
            text="Отметить как выполненное",
            # command=self._complete_task,
            state=DISABLED
        )
        self.done_button.pack(side=LEFT, padx=5)

        self.delete_button = ttk.Button(
            self.button_frame,
            text="Удалить",
            # command=self._delete_task,
            state=DISABLED
        )
        self.delete_button.pack(side=LEFT, padx=5)


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = ToDoApp(root)
    app.run()
