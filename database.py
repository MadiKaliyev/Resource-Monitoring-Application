import sqlite3

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.setup()

    def setup(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                cpu_usage REAL,
                ozu_usage REAL,
                ozu_free REAL,
                ozu_total REAL,
                pzu_usage REAL,
                pzu_free REAL,
                pzu_total REAL
            )
        """)
        self.conn.commit()

    def insert_record(self, data):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO records (timestamp, cpu_usage, ozu_usage, ozu_free, ozu_total, pzu_usage, pzu_free, pzu_total) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        self.conn.commit()

    def get_history(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM records")
        return cursor.fetchall()

    def close(self):
        self.conn.close()
