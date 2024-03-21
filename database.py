import sqlite3


class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT NOT NULL,
                           password TEXT NOT NULL)"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS entries
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           user_id INTEGER NOT NULL,
                           entry_text TEXT NOT NULL,
                           entry_date TEXT NOT NULL,
                           FOREIGN KEY (user_id) REFERENCES users(id))"""
        )
        self.conn.commit()

    def close(self):
        self.conn.close()
