
import sqlite3
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline


DATABASE_PATH = (
        Path(__file__).resolve().parent / ".." / ".." / "SQLDatabase" / "CarInfoDatabase.db"
).resolve()

FEATURES = [
    "Horse Power",
    "Cylinder Number",
    "Engine Displacement",
    "Kerb Weight"
]

TARGET = "Miles Per Gallon"


def train_model():
    # Connect to the database
    with sqlite3.connect(DATABASE_PATH) as connection:
        query = """
                SELECT
                    "Horse Power",
                    "Cylinder Number",
                    "Engine Displacement",
                    "Kerb Weight",
                    "Miles Per Gallon"
                FROM CarStats \
                """

        data = pd.read_sql_query(query, connection)

    #Convert columns to numeric value
    for column in FEATURES + [TARGET]:
        data[column] = pd.to_numeric(
            data[column]
        )

    X = data[FEATURES]
    y = data[TARGET]

    # Create the regression model
    model = make_pipeline(
        RandomForestRegressor(
            n_estimators=200,
            random_state=42
        )
    )

    model.fit(X, y)

    return model


def predict_mpg(model, horsepower, cylinders,
                displacement, weight):
    #Prepare the new vehicle stats
    car = pd.DataFrame([{
        "Horse Power": horsepower,
        "Cylinder Number": cylinders,
        "Engine Displacement": displacement,
        "Kerb Weight": weight
    }])

    # Return the estimated MPG
    prediction = model.predict(car[FEATURES])[0]

    return float(prediction)
