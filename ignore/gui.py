from tkinter import *
from tkinter import ttk
from task import TaskManager
from tkcalendar import DateEntry


class ToDoApp():
    def __init__(self, root):
        self.root = root

        # Цветовая палитра
        self.colors = {
            'background': '#f5f7fa',
            'primary': '#6c5ce7',
            'primary_light': '#a29bfe',
            'secondary': '#00b894',
            'accent': '#fd79a8',
            'text': '#2d3436',
            'text_light': '#636e72',
            'white': '#ffffff',
            'card': '#dfe6e9'
        }

        self._setup_window()

        # Стиль
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Настройка стилей
        self._configure_styles()

        self.manager = TaskManager()

        # Основные фреймы
        self.main_frame = ttk.Frame(self.root, padding=0)
        self.main_frame.pack(fill=BOTH, expand=True)

        # Левый фрейм для логотипа
        self.logo_frame = ttk.Frame(self.main_frame, padding=20)
        self.logo_frame.pack(side=LEFT, fill=Y, expand=False)
        self.logo_frame.configure(style='Primary.TFrame')

        # Правый фрейм для контента
        self.content_frame = ttk.Frame(self.main_frame, padding=20)
        self.content_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        # Верхняя часть - форма ввода
        self.input_frame = ttk.Frame(self.content_frame, padding=15, style='Card.TFrame')
        self.input_frame.pack(fill=X, pady=(0, 15))

        # Фильтр
        self.filter_frame = ttk.Frame(self.content_frame, padding=10, style='Card.TFrame')
        self.filter_frame.pack(fill=X, pady=(0, 15))

        # Центр - таблица
        self.tree_frame = ttk.Frame(self.content_frame, style='Card.TFrame')
        self.tree_frame.pack(fill=BOTH, expand=True)

        # Низ - кнопки управления
        self.button_frame = ttk.Frame(self.content_frame, padding=10)
        self.button_frame.pack(fill=X, pady=(15, 0))

        # Логотип и текст
        self.logo_text = Label(
            self.logo_frame,
            text="TO DO\nAPP",
            font=('Arial', 24, 'bold'),
            fg=self.colors['white'],
            bg=self.colors['primary'],
            justify=CENTER
        )
        self.logo_text.pack(pady=(20, 10))

        self.logo_text2 = Label(
            self.logo_frame,
            text="DERIN TECH",
            font=('Arial', 12, 'bold'),
            fg=self.colors['white'],
            bg=self.colors['primary'],
            justify=CENTER
        )
        self.logo_text2.pack(pady=(0, 20))

        self._create_widgets()
        self._create_tasks_tree()
        self._load_tasks()

    def _configure_styles(self):
        """Настраиваем стили виджетов"""
        # Фреймы
        self.style.configure('Primary.TFrame', background=self.colors['primary'])
        self.style.configure('Card.TFrame',
                             background=self.colors['card'],
                             relief=RAISED,
                             borderwidth=0)

        # Кнопки
        self.style.configure('TButton',
                             font=('Arial', 10),
                             padding=6,
                             borderwidth=1,
                             relief=FLAT)
        self.style.map('Primary.TButton',
                       foreground=[('active', self.colors['white']),
                                   ('pressed', self.colors['white']),
                                   ('!disabled', self.colors['white'])],
                       background=[('active', self.colors['primary_light']),
                                   ('pressed', self.colors['primary']),
                                   ('!disabled', self.colors['primary'])])

        self.style.map('Accent.TButton',
                       foreground=[('active', self.colors['white']),
                                   ('pressed', self.colors['white']),
                                   ('!disabled', self.colors['white'])],
                       background=[('active', self.colors['accent']),
                                   ('pressed', self.colors['secondary']),
                                   ('!disabled', self.colors['accent'])])

        self.style.map('Secondary.TButton',
                       foreground=[('active', self.colors['white']),
                                   ('pressed', self.colors['white']),
                                   ('!disabled', self.colors['white'])],
                       background=[('active', self.colors['secondary']),
                                   ('pressed', self.colors['primary']),
                                   ('!disabled', self.colors['secondary'])])

        # Поля ввода
        self.style.configure('TEntry',
                             fieldbackground=self.colors['white'],
                             foreground=self.colors['text'],
                             padding=5,
                             relief=FLAT)

        # Combobox
        self.style.configure('TCombobox',
                             fieldbackground=self.colors['white'],
                             foreground=self.colors['text'],
                             padding=5)

        # Treeview
        self.style.configure('Treeview',
                             background=self.colors['white'],
                             foreground=self.colors['text'],
                             fieldbackground=self.colors['white'],
                             rowheight=25,
                             borderwidth=0)

        self.style.configure('Treeview.Heading',
                             font=('Arial', 10, 'bold'),
                             background=self.colors['primary_light'],
                             foreground=self.colors['white'],
                             relief=FLAT)

        self.style.map('Treeview',
                       background=[('selected', self.colors['primary_light'])],
                       foreground=[('selected', self.colors['white'])])

        # Метки
        self.style.configure('TLabel',
                             background=self.colors['card'],
                             foreground=self.colors['text'],
                             font=('Arial', 10))

        # Настройка DateEntry
        self.style.configure('DateEntry',
                             fieldbackground=self.colors['white'],
                             foreground=self.colors['text'],
                             arrowcolor=self.colors['primary'],
                             selectbackground=self.colors['primary_light'])

    def _setup_window(self):
        """Настройка главного окна"""
        self.root.title("To Do App")
        self.root.configure(background=self.colors['background'])

        # Установка размеров окна
        window_width = 900
        window_height = 650

        # Центрирование окна
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(800, 600)

    def _create_widgets(self):
        """Создаем элементы формы ввода"""
        # Новая задача
        ttk.Label(self.input_frame, text="Новая задача:", style='TLabel').grid(row=0, column=0, sticky=W, pady=(0, 5))
        self.entry_task = ttk.Entry(self.input_frame, width=40, style='TEntry')
        self.entry_task.grid(row=0, column=1, padx=5, pady=(0, 5), sticky=EW)

        # Описание
        ttk.Label(self.input_frame, text="Описание:", style='TLabel').grid(row=1, column=0, sticky=W, pady=(0, 5))
        self.description = ttk.Entry(self.input_frame, width=40, style='TEntry')
        self.description.grid(row=1, column=1, padx=5, pady=(0, 5), sticky=EW)

        # Приоритет
        ttk.Label(self.input_frame, text="Приоритет:", style='TLabel').grid(row=2, column=0, sticky=W, pady=(0, 5))
        self.priority = ttk.Combobox(self.input_frame,
                                     values=["Низкий", "Средний", "Высокий"],
                                     width=15,
                                     state="readonly",
                                     style='TCombobox')
        self.priority.grid(row=2, column=1, padx=5, pady=(0, 5), sticky=EW)
        self.priority.current(1)  # Значение по умолчанию "Средний"

        # Срок выполнения
        ttk.Label(self.input_frame, text="Срок выполнения:", style='TLabel').grid(row=3, column=0, sticky=W,
                                                                                  pady=(0, 5))
        date_frame = ttk.Frame(self.input_frame)
        date_frame.grid(row=3, column=1, padx=5, pady=(0, 5), sticky=EW)

        self.due_date = DateEntry(date_frame,
                                  width=15,
                                  background=self.colors['primary'],
                                  foreground='white',
                                  borderwidth=0,
                                  date_pattern="dd.mm.yyyy",
                                  font=('Arial', 10),
                                  state="readonly")
        self.due_date.pack(side=LEFT, fill=X, expand=True)

        # Кнопка очистки даты
        self.clear_date_button = ttk.Button(
            date_frame,
            text="X",
            width=2,
            command=self._clear_due_date,
            style='Accent.TButton'
        )
        self.clear_date_button.pack(side=LEFT, padx=(5, 0))

        # Кнопка добавления
        self.add_button = ttk.Button(
            self.input_frame,
            text="Добавить задачу",
            style='Primary.TButton'
        )
        self.add_button.grid(row=4, column=0, pady=(10, 0), sticky=NSEW, columnspan=2)

        # Фильтр
        ttk.Label(self.filter_frame, text="Фильтр:", style='TLabel').pack(side=LEFT, padx=(0, 5))
        self.filter = ttk.Combobox(self.filter_frame,
                                   values=["Все", "Выполненные", "Невыполненные", "Низкий", "Средний", "Высокий"],
                                   width=20,
                                   state="readonly",
                                   style='TCombobox')
        self.filter.pack(side=LEFT, padx=5)
        self.filter.current(0)

    def _clear_due_date(self):
        """Полностью очищает поле даты"""
        self.due_date._set_text('')
        self.due_date._date = None

    def _create_tasks_tree(self):
        """Создаем таблицу задач"""
        # Создаем Treeview с прокруткой
        tree_container = ttk.Frame(self.tree_frame)
        tree_container.pack(fill=BOTH, expand=True, padx=0, pady=0)

        scrollbar = ttk.Scrollbar(tree_container, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.task_tree = ttk.Treeview(
            tree_container,
            columns=("title", "description", "due_date", "priority", "status"),
            show="headings",
            selectmode="browse",
            yscrollcommand=scrollbar.set,
            style='Treeview'
        )
        self.task_tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.task_tree.yview)

        # Настраиваем заголовки
        self.task_tree.heading("title", text="Задача")
        self.task_tree.heading("description", text="Описание")
        self.task_tree.heading("due_date", text="Срок")
        self.task_tree.heading("priority", text="Приоритет")
        self.task_tree.heading("status", text="Статус")

        # Настраиваем колонки
        self.task_tree.column("title", width=200, anchor=W)
        self.task_tree.column("description", width=250, anchor=W)
        self.task_tree.column("due_date", width=100, anchor=CENTER)
        self.task_tree.column("priority", width=100, anchor=CENTER)
        self.task_tree.column("status", width=100, anchor=CENTER)

        # Кнопки управления в нижнем фрейме
        self.done_button = ttk.Button(
            self.button_frame,
            text="✓ Выполнено",
            style='Secondary.TButton',
            state=DISABLED
        )
        self.done_button.pack(side=LEFT, padx=5)

        self.delete_button = ttk.Button(
            self.button_frame,
            text="✕ Удалить",
            style='Accent.TButton',
            state=DISABLED
        )
        self.delete_button.pack(side=LEFT, padx=5)

        self.add_button.config(command=self._add_task)
        self.done_button.config(command=self._complete_task)
        self.delete_button.config(command=self._delete_task)

        # Привязка выбора задачи
        self.task_tree.bind("<<TreeviewSelect>>", self._on_task_select)

    def _load_tasks(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        tasks = self.manager.get_all_tasks()
        for task in tasks:
            status = "Выполнена" if task['is_done'] else "Не выполнена"
            due_date = task['due_date'] if task['due_date'] else ""

            # Добавляем тег для цветового оформления в зависимости от статуса
            tags = (task['id'],)
            if task['is_done']:
                tags += ('done',)
            else:
                tags += ('pending',)

            self.task_tree.insert("", "end",
                                  values=(task['title'],
                                          task['description'],
                                          due_date,
                                          task['priority'],
                                          status),
                                  tags=tags)

        # Настраиваем цвета для строк
        self.task_tree.tag_configure('done', foreground=self.colors['text_light'])
        self.task_tree.tag_configure('pending', foreground=self.colors['text'])

    def _add_task(self):
        try:
            title = self.entry_task.get()
            description = self.description.get()
            priority = self.priority.get()

            # Проверяем, есть ли дата в поле
            if self.due_date.get():
                due_date = self.due_date.get_date().strftime("%d.%m.%Y")
            else:
                due_date = None

            self.manager.add_task(title, description, priority, due_date)

            # Очищаем поля
            self.entry_task.delete(0, END)
            self.description.delete(0, END)
            self._load_tasks()

        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Ошибка", str(e))

    def _complete_task(self):
        """Отмечает задачу выполненной"""
        selected = self.task_tree.selection()
        if selected:
            task_id = self.task_tree.item(selected[0])['tags'][0]
            self.manager.update_task_status(task_id, True)
            self._load_tasks()

    def _on_task_select(self, event):
        """Активирует кнопки при выборе задачи"""
        if self.task_tree.selection():
            self.done_button.config(state=NORMAL)
            self.delete_button.config(state=NORMAL)
        else:
            self.done_button.config(state=DISABLED)
            self.delete_button.config(state=DISABLED)

    def _delete_task(self):
        """Удаляет задачу с подтверждением"""
        selected = self.task_tree.selection()
        if selected:
            task_id = self.task_tree.item(selected[0])['tags'][0]
            from tkinter import messagebox
            if messagebox.askyesno("Подтверждение", "Удалить выбранную задачу?"):
                self.manager.delete_task(task_id)
                self._load_tasks()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = Tk()
    app = ToDoApp(root)
    try:
        app.run()
    finally:
        app.manager.close()