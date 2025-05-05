from database import Database

class TaskManager():
    def __init__(self):
        self.db = Database()
    def add_task(self, title, description='', priority="Средний", due_date=None):
        if not title.strip():
            raise ValueError("Название задачи не может быть пустым")
        return self.db.add_task(title, description, priority, due_date)

    def get_all_tasks(self): # возвращает ВСЕ задачи в формате для Treeview
        db_tasks = self.db.get_all_tasks()
        return [{
            "id": task[0],
            "title": task[1],
            "description": task[2],
            "is_done": bool(task[3]),
            "due_date": task[4],
            "priority": task[5]
        } for task in db_tasks]

    def delete_task(self, task_id): # удаление задачи по айди
        self.db.delete_task(task_id)

    def update_task_status(self, task_id, is_done=True): # обновление статуса задачи
        self.db.update_task_status(task_id, is_done)

    def update_full_task(self, task_id, title, description, priority, due_date):
        if not title.strip():
            raise ValueError("Название задачи не может быть пустым")
        self.db.update_full_task(task_id, title, description, priority, due_date)

    def close(self): # закрываем соединеие с бд
        self.db.close_db()

