# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()
port = os.getenv("DB_PORT")
password = os.getenv("DB_PASS")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
host = os.getenv("DB_HOST")


class ImmowebPipeline:

    def open_spider(self, spider):
        if spider.name != "most_expensive":
            return
        self.connection = psycopg2.connect(
            host=host, database=database, user=user, password=password, port=port
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
            DROP TABLE IF EXISTS most_expensive;
            CREATE TABLE most_expensive (
                id SERIAL PRIMARY KEY,
                url VARCHAR(255) UNIQUE,
                typeHouse VARCHAR(255),
                checked BOOLEAN DEFAULT FALSE
            )
            """
        )
        self.connection.commit()

    def process_item(self, item, spider):
        if spider.name != "most_expensive":
            return item
        self.cursor.execute(
            """
            INSERT INTO most_expensive (url, typeHouse) VALUES (%s, %s)
            ON CONFLICT (url) DO NOTHING
            """,
            (item["href"], item["title"]),
        )
        self.connection.commit()
        return item

    def close_spider(self, spider):
        if spider.name != "most_expensive":
            return
        self.cursor.close()
        self.connection.close()
