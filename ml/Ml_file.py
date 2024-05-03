import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
from PreMl_file import PreMl
import pandas as pd
from joblib import dump
from joblib import load
import random


class ModelTrainer:
    def __init__(self):
        self.ml = PreMl()
        self.data = self.ml.get_data("pre_ml_data", "*")

    def clean_data(self):
        # Convert self.data to a DataFrame
        data = pd.DataFrame(self.data)

        # Print out the columns
        # print(data.columns)

        # Handle missing values
        # drop rows with missing price
        data = data.dropna(subset=["price"])

        # Remove duplicates
        data = data.drop_duplicates()

        # Remove the ID column
        data = data.drop(columns=["url"])

        if data["property_type"].any() == "APARTMENT":
            # Remove rows with missing values in the following columns
            data = data.drop(columns=["land_surface"])

        # Remove the construction year
        data = data.drop(columns=["construction_year"])

        # Remove the property_type
        data = data.drop(columns=["property_type"])
        return data

    def train_model(self, data):
        # Convert the data to a DataFrame
        df = pd.DataFrame(data)

        # Separate the target variable 'price' from the features
        X = df.drop(columns=["price"])
        y = df["price"]

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

        # Train the model using XGBoost
        model = XGBRegressor()
        model.fit(X_transformed, y)

        # Save the trained model and the preprocessor for later use
        dump(model, "immo_model.joblib")
        dump(preprocessor, "preprocessor.joblib")

        # Return the trained model and the preprocessor
        return model, preprocessor

    def predict(self, input_data):
        # Load the model from the joblib file
        self.model = load("immo_model.joblib")

        if self.model is None:
            raise Exception(
                "No model is found. You must train the model before testing it."
            )

        # Load the preprocessor
        preprocessor = load("preprocessor.joblib")

        # Convert the input data to a DataFrame
        input_df = pd.DataFrame([input_data])

        # Convert boolean columns to int
        bool_cols = [col for col in input_df.columns if input_df[col].dtype == bool]
        input_df[bool_cols] = input_df[bool_cols].astype(int)

        # Preprocess the input data
        input_df_transformed = preprocessor.transform(input_df)

        # Make a prediction
        prediction = self.model.predict(input_df_transformed)

        return prediction[0]
