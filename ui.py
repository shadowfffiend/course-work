from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from task import TaskManager

class ToDoApp():
    def __init__(self, root):
        self.root = root
        self.manager = TaskManager()

        self._setup_window()
        self._setup_style()
        self._create_widgets()
        self._create_tasks_tree()
        self._load_tasks()

    def _setup_style(self):
        self.style = ttk.Style()
        self.style.theme_use("default")

        self.style.configure("TFrame", background="#CADFF6")
        self.style.configure("TLabel", background="#CADFF6", font=('Arial', 11), foreground="#000814")
        self.style.configure("TButton", background="#22577a", foreground="white", font=('Arial', 11))
        self.style.map("TButton", background=[('active', '#2c7be5')])

        self.style.configure("Treeview",
                             background="#eef5fc",
                             foreground="#333333",
                             fieldbackground="eef5fc",
                             font=('Arial', 11),
                             rowheight=30)
        self.style.map("Treeview",
                       background=[('selected', '#d6eaff')],
                       foreground=[('selected', '#0d1b2a')])

        self.style.configure("Treeview.Heading",
                             font=('Arial', 10, 'bold'),
                             background="#22577a",
                             foreground="white")
        self.style.map("Treeview.Heading",
                       background=[('selected', '#d6eaff')],
                       foreground=[('selected', '#0d1b2a')])

        self.style.configure("TCombobox",
                             font=('Arial', 13))

        self.style.map("TCombobox",
                       fieldbackground=[("readonly", "#EEF5FC")],
                       background=[("readonly", "#EEF5FC")])

        self.style.configure("Vertical.TScrollbar",
                             troughcolor="#EEF5FC",
                             relief=RAISED)

        self.style.map("Vertical.TScrollbar", background=[('active', '#CADFF6'), ('!active', '#CADFF6')])

    def _create_widgets(self):
        self.input_frame = ttk.Frame(self.root, padding=(10, 5))
        self.input_frame.pack(fill=BOTH, expand=True)  # Верхняя часть - форма ввода

        self.filter_frame = ttk.Frame(self.root, padding=(10, 0))
        self.filter_frame.pack(fill=BOTH, expand=True)  # размещаем фильтр между формой ввода и таблицей

        self.tree_frame = ttk.Frame(self.root, padding=(10, 1))
        self.tree_frame.pack(fill=BOTH, expand=True)  # центр - таблица

        self.button_frame = ttk.Frame(self.root, padding=(10, 5))
        self.button_frame.pack(fill=BOTH, expand=True)  # низ - кнопки управления

        self.logo_text = Label(
            self.root,
            text="TO DO\n✅APP",
            font=('Arial', 40, 'bold'),
            bg='#CADFF6',
            fg='#0d1b2a',  # цвет
            justify=RIGHT,  # выравнивание
            padx=50,
            pady=5
        )
        self.logo_text2 = Label(
            self.root,
            text="PRIME TECH",
            font=('Arial', 15, 'bold'),  # Шрифт как на скриншоте
            bg='#CADFF6',
            fg='#0d1b2a',  # Цвет текста
            justify=RIGHT,  # Выравнивание по правому краю
            padx=50,  # Отступы
            pady=5
        )
        self.logo_text.place(relx=1.0, rely=0.0, anchor=NE, x=-10, y=10)
        self.logo_text2.place(relx=1.0, rely=0.0, anchor=NE, x=-10, y=150)

        """Создаем элементы формы ввода"""
        # Новая задача
        ttk.Label(self.input_frame, text="Новая задача:").grid(row=0, column=0, sticky=W)
        self.entry_task = Entry(self.input_frame, width=40, font=('Arial', 13), bg="#EEF5FC", fg="#000814")
        self.entry_task.grid(row=0, column=1, padx=5, pady=5)

        def validate(new_value, max_length):
            return len(new_value) <= max_length # возвращает тру фолс

        validate_task = (self.root.register(lambda new_value: validate(new_value, 30)), "%P")
        self.entry_task = Entry(self.input_frame, width=40, font=('Arial', 13), bg="#EEF5FC", fg="#000814",
                                validate="key", validatecommand=validate_task)
        self.entry_task.grid(row=0, column=1, padx=5, pady=5)

        # Описание
        ttk.Label(self.input_frame, text="Описание:").grid(row=1, column=0, sticky=W)
        validate_description = (self.root.register(lambda new_value: validate(new_value, 30)), "%P")
        self.description = Entry(self.input_frame, width=40, font=('Arial', 13), bg="#EEF5FC", fg="#000814",
                                 validate="key", validatecommand=validate_description)
        self.description.grid(row=1, column=1, padx=5, pady=5)

        # Приоритет
        ttk.Label(self.input_frame, text="Приоритет:").grid(row=2, column=0, sticky=W)
        self.priority = ttk.Combobox(self.input_frame,
                                     values=["Низкий", "Средний", "Высокий"],
                                     width=15,
                                     state="readonly",
                                     font=('Arial', 13))
        self.priority.grid(row=2, column=1, padx=5, pady=5, sticky=EW)
        self.priority.current(1)  # по умолчанию средний

        # Срок выполнения
        ttk.Label(self.input_frame, text="Срок выполнения:").grid(row=3, column=0, sticky=W)
        self.due_date = DateEntry(self.input_frame,
                                  width=15,
                                  borderwidth=2,
                                  date_pattern="dd.mm.yyyy",
                                  font=('Arial', 13),
                                  state="readonly",
                                  background="#163950"
                                  )

        self.due_date.grid(row=3, column=1, padx=5, pady=5, sticky=EW)

        # Кнопка очистки даты
        self.clear_date_button = ttk.Button(
            self.input_frame,
            text="X",
            width=2,
            command=self._clear_due_date
        )
        self.clear_date_button.grid(row=3, column=2, sticky=W)

        # Кнопка добавления
        self.add_button = ttk.Button(
            self.input_frame,
            text="Добавить",
        )
        self.add_button.grid(row=4, column=0, pady=10, sticky=NSEW, columnspan=2)

        # Фильтр
        ttk.Label(self.filter_frame, text="Фильтр:").pack(side=LEFT, padx=5, pady=5)
        self.filter = ttk.Combobox(self.filter_frame,
                                   values=["Все", "Выполненные", "Невыполненные", "Низкий", "Средний", "Высокий"],
                                   width=20,
                                   state="readonly",
                                   font=('Arial', 13))
        self.filter.pack(side=LEFT, padx=5, pady=5)
        self.filter.current(0)
        self.filter.bind("<<ComboboxSelected>>", self._apply_filter) # привязывает обработчик события выбора нового значения в фильтре

    def _clear_due_date(self):
        """Полностью очищает поле даты"""
        self.due_date._set_text('')
        self.due_date._date = None

    def _setup_window(self):  # main окно
        self.root.title("To Do app")
        window_width = 900
        window_height = 700

        # Центрирование окна
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(850, 600) #  self.root.minsize(700, 600)
        # self.root.maxsize(800, 600) #  self.root.maxsize(800, 700)

    def _apply_filter(self, event=None):
        """Применяет выбранный фильтр к списку задач"""
        filter_value = self.filter.get()
        tasks = self.manager.get_all_tasks()  # Получаем все задачи из БД

        # Очищаем текущее отображение, чтобы потом заново отобразить только те, что подходят под фильтр.
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        # Фильтруем задачи в зависимости от выбранного значения
        for task in tasks:
            status = "Выполнена" if task['is_done'] else "Не выполнена"
            due_date = task['due_date'] if task['due_date'] else ""

            # Проверяем соответствие фильтру
            show_task = True
            if filter_value == "Выполненные" and not task['is_done']:
                show_task = False
            elif filter_value == "Невыполненные" and task['is_done']:
                show_task = False
            elif filter_value in ["Низкий", "Средний", "Высокий"] and task['priority'] != filter_value:
                show_task = False

            if show_task: # если задача прошла фильтр, то:
                self.task_tree.insert("", "end",
                                      values=(task['title'],
                                              task['description'],
                                              due_date,
                                              task['priority'],
                                              status),
                                      tags=(task['id']))

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
        self.task_tree.column("title", width=235)
        self.task_tree.column("description", width=255)
        self.task_tree.column("due_date", width=85)
        self.task_tree.column("priority", width=90)
        self.task_tree.column("status", width=100)

        # Добавляем прокрутку
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set) # связываем вертикальную прокрутку в task_tree с поведением скроллбара

        # Размещаем таблицу и скроллбар
        self.task_tree.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
        scrollbar.pack(side=RIGHT, fill=Y, ipadx=5)

        # Кнопки управления в нижнем фрейме
        self.done_button = ttk.Button(
            self.button_frame,
            text="Отметить как выполненную",
            state=DISABLED
        )
        self.done_button.pack(side=LEFT, padx=5)

        self.delete_button = ttk.Button(
            self.button_frame,
            text="Удалить",
            state=DISABLED
        )
        self.delete_button.pack(side=LEFT, padx=5)

        self.add_button.config(command=self._add_task) # связываем кнопку add_button с функцией _add_task и аналогично для др
        self.done_button.config(command=self._complete_task)
        self.delete_button.config(command=self._delete_task)

        # Привязка выбора задачи
        self.task_tree.bind("<<TreeviewSelect>>", self._on_task_select)

    def _load_tasks(self):
        for item in self.task_tree.get_children(): # очищение таблицы от всех текущих строк перед тем, как загрузить новые
            self.task_tree.delete(item)
        tasks = self.manager.get_all_tasks()
        for task in tasks:
            status = "Выполнена" if task['is_done'] else "Не выполнена"
            due_date = task['due_date'] if task['due_date'] else ""
            self.task_tree.insert("", "end",
                                  values=(task['title'],
                                          task['description'],
                                          due_date,  # Используем обработанное значение
                                          task['priority'],
                                          status),
                                  tags=(task['id']))

    def _add_task(self):
        try:
            # получаем значения из полей ввода
            title = self.entry_task.get()
            description = self.description.get()
            priority = self.priority.get()

            # проверяем, есть ли дата в поле
            if self.due_date.get():
                due_date = self.due_date.get_date().strftime("%d.%m.%Y")
            else:
                due_date = None  # если дата не указана, устанавливаем значение None

            self.manager.add_task(title, description, priority, due_date) # добавляем задачу в базу данных через менеджер

            # очищаем поля ввода после добавления задачи
            self.entry_task.delete(0, END)
            self.description.delete(0, END)
            self._load_tasks() # обновляем таблицу задач, чтобы отобразить добавленную задачу

        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Ошибка", str(e))

    def _complete_task(self):
        """Переключает статус задачи между выполненной и невыполненной"""
        selected = self.task_tree.selection()  # возвращает id выбранной строки в таблице
        if selected:  # Проверяем, выбрана ли задача
            task_id = self.task_tree.item(selected[0])['tags'][0]  # Извлекаем уникальный ID задачи из тега выбранной строки
            current_status = self.task_tree.item(selected[0])['values'][4] == "Выполнена"  # Проверяем, выполнена ли задача (статус в столбце 'status')
            self.manager.update_task_status(task_id, not current_status)  # Инвертируем статус (если выполнена, ставим невыполненную и наоборот)
            self._load_tasks()  # Обновляем отображение задач в таблице

    def _on_task_select(self, event):
        """Активирует кнопки при выборе задачи и меняет текст кнопки в зависимости от статуса"""
        if self.task_tree.selection():
            selected = self.task_tree.selection()[0]
            current_status = self.task_tree.item(selected)['values'][4] == "Выполнена"
            # Меняем текст кнопки в зависимости от статуса
            self.done_button.config(
                text="Отметить как невыполненную" if current_status else "Отметить как выполненную",
                state=NORMAL
            )
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

from tkinter import Tk

if __name__ == "__main__":
    root = Tk()
    app = ToDoApp(root)
    try:
        app.run()
    finally:
        app.manager.close()