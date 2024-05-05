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
import pickle

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
        return houses, apartments

    def clean_data(self, data):
        # Convert self.data to a DataFrame
        data = pd.DataFrame(data)

        # Create a dictionary mapping raw column names to clean column names
        column_name_mapping = dict(zip(self.raw_column_names, self.clean_column_names))

        # Rename the columns
        data = data.rename(columns=column_name_mapping)

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

        return data

    def preprocess_data(self, data):
        # Convert the data to a DataFrame
        data = pd.DataFrame(data=data)

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

    def save_pre_pickle(self, data, filename):
        # Open the file in write binary mode
        with open(filename, "wb") as f:
            # Dump the data into the file
            pickle.dump(data, f)
