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
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()

    def get_data(self, table, columns):
        try:
            self.cur = self.conn.cursor(cursor_factory=DictCursor)
            query = f"SELECT {columns} FROM {table}"
            print(f"Executing query: {query}")
            self.cur.execute(query)
            result = [dict(row) for row in self.cur.fetchall()]
            print(f"Number of rows returned: {len(result)}")
            if not result:
                print(f"No data found for table {table} and columns {columns}")
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
