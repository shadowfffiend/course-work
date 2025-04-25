from database import Database

class TaskManager():
    def __init__(self):
        self.db = Database()
    def add_task(self, title, description='', priority="Средний", due_date=None):
        if not title.strip():
            raise ValueError("Название задачи не может быть пустым")
        return self.db.add_task(title, description, priority, due_date)

    def get_all_tasks(self):
        """Возвращает задачи в формате для Treeview"""
        db_tasks = self.db.get_all_tasks()
        tasks = []
        for task in db_tasks:
            tasks.append({
                "id": task[0],
                "title": task[1],
                "description": task[2],
                "is_done": bool(task[3]),
                "due_date": task[4],
                "priority": task[5]
            })
        return tasks

    def delete_task(self, task_id):
        """Удаляет задачу по ID"""
        self.db.delete_task(task_id)

    def update_task_status(self, task_id, is_done=True):
        """Обновляет статус задачи"""
        self.db.update_task_status(task_id, is_done)

    def close(self):
        """Закрывает соединение с БД"""
        self.db.close_db()