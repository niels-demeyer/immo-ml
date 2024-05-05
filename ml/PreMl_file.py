from dotenv import load_dotenv
import os
import psycopg2
import pandas as pd
from psycopg2.extras import DictCursor
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split

load_dotenv()


class PreMl:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        self.raw_column_names = [
            "url",
            "raw_price_accessibilityprice",
            "raw_property_bathroomcount",
            "raw_property_building_condition",
            "raw_property_building_constructionyear",
            "raw_property_constructionpermit_floodzonetype",
            "raw_property_energy_heatingtype",
            "raw_property_gardensurface",
            "raw_property_hasbasement",
            "raw_property_hasswimmingpool",
            "raw_property_hasterrace",
            "raw_property_land_surface",
            "raw_property_location_district",
            "raw_property_location_locality",
            "raw_property_location_postalcode",
            "raw_property_nethabitablesurface",
            "raw_property_roomcount",
            "raw_property_subtype",
            "raw_property_type",
            "raw_transaction_certificates_renovationobligation",
            "raw_transaction_sale_cadastralincome",
            "raw_transaction_sale_isfurnished",
        ]

        self.clean_column_names = [
            "url",
            "price",
            "bathroom_count",
            "building_condition",
            "construction_year",
            "floodzone_type",
            "heating_type",
            "garden_surface",
            "has_basement",
            "has_swimming_pool",
            "has_terrace",
            "land_surface",
            "district",
            "locality",
            "postal_code",
            "net_habitable_surface",
            "room_count",
            "property_subtype",
            "property_type",
            "renovation_obligation",
            "cadastral_income",
            "is_furnished",
        ]

        self.clean_sql_column_types = {
            "url": "TEXT",
            "price": "INTEGER",
            "bathroom_count": "INTEGER",
            "building_condition": "TEXT",
            "construction_year": "INTEGER",
            "floodzone_type": "TEXT",
            "heating_type": "TEXT",
            "garden_surface": "INTEGER",
            "has_basement": "BOOLEAN",
            "has_swimming_pool": "BOOLEAN",
            "has_terrace": "BOOLEAN",
            "land_surface": "INTEGER",
            "district": "TEXT",
            "locality": "TEXT",
            "postal_code": "INTEGER",
            "net_habitable_surface": "INTEGER",
            "room_count": "INTEGER",
            "property_subtype": "TEXT",
            "property_type": "TEXT",
            "renovation_obligation": "BOOLEAN",
            "cadastral_income": "INTEGER",
            "is_furnished": "BOOLEAN",
        }

        self.cur = self.conn.cursor()
        self.data = self.get_data("ml_data", "*")  # Fetch data from the ml_data table

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

    def split_data_property_type(self, data):
        # Convert self.data to a DataFrame
        data = pd.DataFrame(data)
        print(data.columns)
        print(data.shape)

        # Print out the options for the raw_property_type column
        print(data["raw_property_subtype"].unique())

        # Split into houses and apartments
        houses = data[data["raw_property_type"] == "house"]
        apartments = data[data["raw_property_type"] == "apartment"]

    def join_ml_data(self):
        try:
            self.cur = self.conn.cursor(cursor_factory=DictCursor)

            # Specify the columns to join
            columns_to_join = [
                "url",
                "raw_price_accessibilityprice",
                "raw_property_bathroomcount",
                "raw_property_building_condition",
                "raw_property_building_constructionyear",
                "raw_property_constructionpermit_floodzonetype",
                "raw_property_energy_heatingtype",
                "raw_property_gardensurface",
                "raw_property_hasbasement",
                "raw_property_hasswimmingpool",
                "raw_property_hasterrace",
                "raw_property_land_surface",
                "raw_property_location_district",
                "raw_property_location_locality",
                "raw_property_location_postalcode",
                "raw_property_nethabitablesurface",
                "raw_property_roomcount",
                "raw_property_subtype",
                "raw_property_type",
                "raw_transaction_certificates_renovationobligation",
                "raw_transaction_sale_cadastralincome",
                "raw_transaction_sale_isfurnished",
            ]

            # Create new table with all columns set to TEXT
            columns = ", ".join([f"{col} TEXT" for col in columns_to_join])
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

    def save_to_pre_ml_data(self, data):
        try:
            # Create table if it doesn't exist
            create_table_query = """
            CREATE TABLE IF NOT EXISTS pre_ml_data (
                url TEXT PRIMARY KEY,
                price INTEGER,
                bathroom_count INTEGER,
                building_condition TEXT,
                construction_year INTEGER,
                floodzone_type TEXT,
                heating_type TEXT,
                garden_surface INTEGER,
                has_basement BOOLEAN,
                has_swimming_pool BOOLEAN,
                has_terrace BOOLEAN,
                land_surface INTEGER,
                district TEXT,
                locality TEXT,
                postal_code INTEGER,
                net_habitable_surface INTEGER,
                room_count INTEGER,
                property_subtype TEXT,
                property_type TEXT,
                renovation_obligation BOOLEAN,
                cadastral_income INTEGER,
                is_furnished BOOLEAN
            );
            """
            self.cur.execute(create_table_query)

            # Insert data into table
            for row in data:
                placeholders = ", ".join(["%s"] * len(row))
                columns = ", ".join(row.keys())
                values = tuple(row.values())
                query = f"""
                INSERT INTO pre_ml_data ({columns}) VALUES ({placeholders})
                ON CONFLICT (url) DO NOTHING
                """
                self.cur.execute(query, values)

            # Commit the changes
            self.conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()  # Rollback the transaction in case of an error

    def clean_data(self, data):
        # Convert self.data to a DataFrame
        data = pd.DataFrame(data)

        # Print out the columns
        print(data.columns)

        # Handle missing values
        # drop rows with missing price
        data = data.dropna(subset=["price"])

        # Remove duplicates
        data = data.drop_duplicates()

        # Remove the ID column
        data = data.drop(columns=["url"])

        # Remove the construction year
        data = data.drop(columns=["construction_year"])

    def preprocess_data(self):
        # Convert the data to a DataFrame
        data = pd.DataFrame(self.data)

        # Separate the target variable 'price' from the features
        X = data.drop(columns=["price"])
        y = data["price"]

        # Define preprocessing steps
        numeric_features = X.select_dtypes(include=["int64", "float64"]).columns
        categorical_features = X.select_dtypes(include=["object"]).columns
        boolean_features = X.select_dtypes(include=["bool"]).columns

        # Convert boolean columns to int
        X[boolean_features] = X[boolean_features].astype(int)

        numeric_transformer = make_pipeline(
            SimpleImputer(strategy="median"), StandardScaler()
        )

        categorical_transformer = make_pipeline(
            SimpleImputer(strategy="constant", fill_value="missing"),
            OneHotEncoder(handle_unknown="ignore"),
        )

        boolean_transformer = SimpleImputer(strategy="most_frequent")

        preprocessor = make_column_transformer(
            (numeric_transformer, numeric_features),
            (categorical_transformer, categorical_features),
            (boolean_transformer, boolean_features),
        )

        # Fit and transform the features DataFrame
        X_transformed = preprocessor.fit_transform(X)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X_transformed, y, test_size=0.2, random_state=42
        )

        return X_train, X_test, y_train, y_test
