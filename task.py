class TaskManager():
    def __init__(self):
        self.tasks = []
    def add_task(self, title, description='', priority="Средний"):
        self.tasks.append({
            "id": len(self.tasks) + 1,
            "title":title,
            "description":description,
            "priority":priority,
            "is_done": False
        })
    def get_all_tasks(self):
        return self.tasks
    def delete_task(self, task_id): pass
    def update_task_status(self, task_id): pass
