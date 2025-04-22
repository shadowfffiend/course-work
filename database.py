import sqlite3 as sq

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
            is_done boolean default 0,
            priority text check (priority in ('Нет','Низкий','Средний','Высокий'))
        )
        """)
        self.conn.commit()
    def add_task(self, title, description='', priority='Нет'):
        self.cursor.execute("""
        INSERT INTO tasks VALUES (
            
        )
        """)
table1 = Database()