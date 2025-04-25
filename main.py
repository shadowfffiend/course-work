from tkinter import Tk
from ui import ToDoApp

if __name__ == "__main__":
    root = Tk()
    app = ToDoApp(root)
    try:
        app.run()
    finally:
        app.manager.close()


