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
from joblib import dump as joblib
from joblib import load as load_joblib
import random


class ModelTrainer:
    def __init__(self):
        self.ml = PreMl()

    def train_model(self):
        # Preprocess the data
        data = self.ml.get_data("pre_ml_data", "*")
        df = pd.DataFrame(data)

        # Define preprocessing steps
        numeric_features = df.select_dtypes(include=["int64", "float64"]).columns
        categorical_features = df.select_dtypes(include=["object"]).columns
        boolean_features = df.select_dtypes(include=["bool"]).columns

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

        # Split the data
        X = df.drop("price", axis=1)
        y = df["price"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Define the model
        model = make_pipeline(
            preprocessor, XGBRegressor(objective="reg:squarederror", random_state=42)
        )

        # Train the model
        model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        print(f"RMSE: {rmse}")

        # Save the model
        joblib.dump(model, "model_immo.joblib")

    def test_model(self, X_test, y_test):
        # Load the model from the joblib file
        self.model = load_joblib("model_immo.joblib")

        if self.model is None:
            raise Exception(
                "No model is found. You must train the model before testing it."
            )

        # Predict the test data
        y_pred = self.model.predict(X_test)

        # Evaluate the model
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        print(f"RMSE: {rmse}")

        return rmse
