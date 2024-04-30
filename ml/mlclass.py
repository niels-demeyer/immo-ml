from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import DictCursor

load_dotenv()


class MLClass:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()

    def get_data(self, table, columns):
        self.cur = self.conn.cursor(cursor_factory=DictCursor)
        self.cur.execute(f"SELECT {columns} FROM {table}")
        return [dict(row) for row in self.cur.fetchall()]
