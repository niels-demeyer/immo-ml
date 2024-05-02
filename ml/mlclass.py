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
        
    def join_ml_data(self):
        try:
            self.cur = self.conn.cursor(cursor_factory=DictCursor)
            
            # Specify the columns to join
            columns_to_join = [
                'url',
                'raw_price_accessibilityprice',
                'raw_property_bathroomcount',
                'raw_property_building_condition',
                'raw_property_building_constructionyear',
                'raw_property_constructionpermit_floodzonetype',
                'raw_property_energy_heatingtype',
                'raw_property_gardensurface',
                'raw_property_hasbasement',
                'raw_property_hasswimmingpool',
                'raw_property_hasterrace',
                'raw_property_land_surface',
                'raw_property_location_district',
                'raw_property_location_locality',
                'raw_property_location_postalcode',
                'raw_property_nethabitablesurface',
                'raw_property_roomcount',
                'raw_property_subtype',
                'raw_property_type',
                'raw_transaction_certificates_renovationobligation',
                'raw_transaction_sale_cadastralincome',
                'raw_transaction_sale_isfurnished'
            ]

            # Create new table with all columns set to TEXT
            columns = ', '.join([f"{col} TEXT" for col in columns_to_join])
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS ml_data (
                {columns}
            );
            """
            self.cur.execute(create_table_query)

            # Copy distinct rows from the existing table to the new table
            query = f"INSERT INTO ml_data SELECT DISTINCT {', '.join(columns_to_join)} FROM raw_data_table"
            self.cur.execute(query)
            self.conn.commit()  # Commit the INSERT statement

            # Fetch all rows from the new table
            self.cur.execute("SELECT * FROM ml_data")
            result = [dict(row) for row in self.cur.fetchall()]
            print(f"Number of rows returned: {len(result)}")
            if not result:
                print(f"No data found for table ml_data")
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()  # Rollback the transaction in case of an error
            return []
    def preprocess_data(self):
        try:
            ml_data = self.get_data("ml_data", "*")
            return ml_data
        except Exception as e:
            print(f"An error occurred: {e}")
            return []