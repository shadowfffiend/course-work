from tkinter import *

from task import TaskManager


class ToDoApp():
    def __init__(self, root):
        self.root = root
        self.root.title("To Do")

        self.manager = TaskManager()  # подключаем менеджер


    def zxc(self):
        self.root.mainloop()
root = Tk()
okno1 = ToDoApp(root)
okno1.zxc()


