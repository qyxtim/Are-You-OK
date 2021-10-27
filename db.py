import sqlite3


class open_db:
    def __init__(self, db_name):
        self.name = db_name

    def __enter__(self):
        self.db = sqlite3.connect(self.name, check_same_thread=False)
        self.cursor = self.db.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, trace):
        self.db.commit()
        self.cursor.close()
        self.db.close()
