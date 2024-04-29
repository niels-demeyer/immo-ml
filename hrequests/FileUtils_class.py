import os
import shutil
import json
import csv
import sqlite3
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
port = os.getenv("DB_PORT")
password = os.getenv("DB_PASS")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
host = os.getenv("DB_HOST")



class FileUtils:
    @staticmethod
    def flatten_dict(d, parent_key="", sep="_"):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(FileUtils.flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                for i, elem in enumerate(v):
                    if isinstance(elem, dict):
                        items.extend(
                            FileUtils.flatten_dict(
                                elem, f"{new_key}{sep}{i}", sep=sep
                            ).items()
                        )
                    else:
                        items.append((f"{new_key}{sep}{i}", elem))
            else:
                items.append((new_key, v))
        return dict(items)

    @staticmethod
    def write_dict_to_csv(file_path, data):
        # Check if data is a list
        if isinstance(data, list):
            # Flatten each dictionary in the list
            flat_data_list = [FileUtils.flatten_dict(item) for item in data]
        else:
            # If data is not a list, assume it's a dictionary and flatten it
            flat_data_list = [FileUtils.flatten_dict(data)]

        # Get all keys used in any dictionary
        all_keys = set().union(*(d.keys() for d in flat_data_list))

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=all_keys)
                writer.writeheader()
                for flat_data in flat_data_list:
                    writer.writerow(flat_data)
        except UnicodeEncodeError as e:
            print(f"UnicodeEncodeError: {e}")
            
    def write_dict_to_postgres(table_name, data):
        # Create a connection to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )

        # Create a cursor object
        cur = conn.cursor()

        # Check if data is a list
        if isinstance(data, list):
            # Flatten each dictionary in the list
            flat_data_list = [FileUtils.flatten_dict(item) for item in data]
        else:
            # If data is not a list, assume it's a dictionary and flatten it
            flat_data_list = [FileUtils.flatten_dict(data)]

        # Normalize keys and get all keys used in any dictionary
        all_keys = set().union(*(d.keys() for d in flat_data_list))
        normalized_keys = [key.strip().lower() for key in all_keys]

        # Create table if not exists
        columns = ", ".join(f"{key} text" for key in normalized_keys)
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        )

        # Insert data into table
        for flat_data in flat_data_list:
            # Normalize keys in flat_data
            normalized_data = {
                key.strip().lower(): value for key, value in flat_data.items()
            }
            # Ensure normalized_data has a value for each key in normalized_keys
            values = [normalized_data.get(key, None) for key in normalized_keys]
            placeholders = ", ".join("%s" for _ in normalized_keys)
            sql = f"INSERT INTO {table_name} ({', '.join(normalized_keys)}) VALUES ({placeholders})"
            cur.execute(sql, values)

        # Commit changes and close connection
        conn.commit()
        conn.close()

    @staticmethod
    def write_dict_to_sqlite(db_path, table_name, data):
        # Create a connection to the SQLite database
        conn = sqlite3.connect(db_path)

        # Create a cursor object
        cur = conn.cursor()

        # Check if data is a list
        if isinstance(data, list):
            # Flatten each dictionary in the list
            flat_data_list = [FileUtils.flatten_dict(item) for item in data]
        else:
            # If data is not a list, assume it's a dictionary and flatten it
            flat_data_list = [FileUtils.flatten_dict(data)]

        # Normalize keys and get all keys used in any dictionary
        all_keys = set().union(*(d.keys() for d in flat_data_list))
        normalized_keys = [key.strip().lower() for key in all_keys]

        # Create table if not exists
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(normalized_keys)})"
        )

        # Dynamically alter table to add missing columns
        cur.execute(f"PRAGMA table_info({table_name})")
        existing_columns = [column[1] for column in cur.fetchall()]
        for key in normalized_keys:
            if key not in existing_columns:
                cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {key}")

        # Insert data into table
        for flat_data in flat_data_list:
            # Normalize keys in flat_data
            normalized_data = {
                key.strip().lower(): value for key, value in flat_data.items()
            }
            # Ensure normalized_data has a value for each key in normalized_keys
            values = [normalized_data.get(key, None) for key in normalized_keys]
            placeholders = ", ".join("?" * len(normalized_keys))
            sql = f"INSERT INTO {table_name} ({', '.join(normalized_keys)}) VALUES ({placeholders})"
            cur.execute(sql, values)

        # Commit changes and close connection
        conn.commit()
        conn.close()

    @staticmethod
    def read_json_file(file_path, encoding="utf-8"):
        with open(file_path, "r", encoding=encoding) as f:
            return json.load(f)

    def check_duplicates_json_file(file_path, data):
        with open(file_path, "r") as f:
            old_data = json.load(f)
            for d in data:
                if d not in old_data:
                    old_data.append(d)
        with open(file_path, "w") as f:
            json.dump(old_data, f, indent=4)

    def return_solo_items(data):
        solo_items = []
        for item in data:
            if "href" in item:
                if item["href"] not in solo_items:
                    solo_items.append(item["href"])
        return solo_items

    @staticmethod
    def create_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def remove_directory(directory):
        if os.path.exists(directory):
            shutil.rmtree(directory)

    @staticmethod
    def copy_file(src, dst):
        shutil.copyfile(src, dst)

    @staticmethod
    def move_file(src, dst):
        shutil.move(src, dst)

    @staticmethod
    def remove_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def list_files(directory):
        return os.listdir(directory)

    @staticmethod
    def list_files_with_extension(directory, extension):
        return [f for f in os.listdir(directory) if f.endswith(extension)]
