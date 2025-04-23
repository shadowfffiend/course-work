from tkinter import *
from tkinter import ttk
from task import TaskManager
from tkcalendar import DateEntry

class ToDoApp():
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x600")
        self.root.title("To Do")

        # стиль
        self.style = ttk.Style()
        self.style.theme_use('xpnative')  # clam

        # элементы
        self._create_widgets()

        self.manager = TaskManager()  # подключаем менеджер


    def _create_widgets(self):
        # новая задача
        ttk.Label(self.root, text="Новая задача:", padding=5).grid(row=0, column=0, sticky=W)
        self.entry_task = ttk.Entry(self.root, width=40)
        self.entry_task.grid(row=0, column=1, padx=5, pady=5)

        # описание
        ttk.Label(self.root, text="Описание:", padding=5).grid(row=1, column=0, sticky=W)
        self.description = ttk.Entry(self.root, width=40)
        self.description.grid(row=1, column=1, padx=5, pady=5)

        # приоритет
        ttk.Label(self.root, text="Приоритет:", padding=5).grid(row=2, column=0, sticky=W)
        self.priority = ttk.Combobox(self.root, values=["Низкий", "Средний", "Высокий"], width=15)
        self.priority.grid(row=2, column=1, padx=5, pady=5, sticky=W)

        # срок выполнения
        ttk.Label(self.root, text="Срок выполнения:", padding=5).grid(row=3, column=0, sticky=W)
        self.due_date = DateEntry(self.root,
                                  width=15,
                                  background="gray",
                                  foreground='white',
                                  borderwidth=2,
                                  date_pattern="dd.mm.yyyy")
        self.due_date.grid(row=3, column=1, padx=5, pady=5, sticky="w")



        # кнопка добавления
        self.add_button = ttk.Button(
            self.root,
            text="Добавить",
            # command=self.add_task
        )
        self.add_button.grid(row=4, column=1, pady=10, sticky=EW)

    def zxc(self):
        self.root.mainloop()
root = Tk()
okno1 = ToDoApp(root)
okno1.zxc()


