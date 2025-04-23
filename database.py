import sqlite3 as sq

class Database():
    def __init__(self):
        self.conn = sq.connect("todo.db")
        self.cursor = self.conn.cursor()
        self._create_table()
    def _create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id integer primary key autoincrement,
            title text not null,
            description text,
            is_done integer default 0 check (is_done in (0, 1)),
            due_date text,
            priority text check (priority in ('Низкий','Средний','Высокий')) default  'Средний'
        )
        """)
        self.conn.commit()

    def add_task(self, title, description='', priority='Средний', due_date=None):
        self.cursor.execute("""
            INSERT INTO tasks (title, description, priority, due_date)
            VALUES (?, ?, ?, ?)
            """, (title, description, priority, due_date))
        self.conn.commit()
        return self.cursor.lastrowid

    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def get_all_tasks(self):
        self.cursor.execute("SELECT * FROM tasks")
        return self.cursor.fetchall()

    def update_task_status(self, task_id, is_done):
        self.cursor.execute("""
                    UPDATE tasks SET is_done = ? WHERE id = ?
                    """, (1 if is_done else 0, task_id))
        self.conn.commit()
    def close_db(self):
        self.conn.close()
# table1 = Database()
# table1.add_task("SD","SD", "Низкий")
# table1.add_task('233', "SD", "Низкий")
# table1.delete_task(5)


# connection = sq.connect("todo.db")
#
# cur = connection.cursor()
#
# # cur.execute("""CREATE TABLE IF NOT EXISTS tasks (
# #     id INTEGER,
# #     title TEXT
# # )
# # """)
# #
# # cur.execute("INSERT INTO tasks VALUES (1, 'asda')")
# cur.execute("SELECT rowid, id FROM tasks")
# print(cur.fetchall())
# connection.commit()
#
# connection.close()