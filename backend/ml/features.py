import numpy as np
import pandas as pd

from ml.constants import (
    CLIENT_ID_COLUMN,
    ENGINEERED_NUMERIC_FEATURES,
    FEATURE_COLUMNS,
    LEAKAGE_COLUMNS,
    POSITIVE_CLASS_LABEL,
    PREDICTION_PAYLOAD_RENAME_MAP,
    TARGET_COLUMN,
)


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = [column.strip() for column in cleaned.columns]
    return cleaned.drop(columns=[column for column in LEAKAGE_COLUMNS if column in cleaned.columns])


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    featured = df.copy()
    featured["Balance_To_Limit_Ratio"] = np.divide(
        featured["Total_Revolving_Bal"],
        featured["Credit_Limit"].replace(0, np.nan),
    ).fillna(0)
    featured["Average_Transaction_Value"] = np.divide(
        featured["Total_Trans_Amt"],
        featured["Total_Trans_Ct"].replace(0, np.nan),
    ).fillna(0)
    featured["Relationship_Depth_Per_Year"] = np.divide(
        featured["Total_Relationship_Count"],
        (featured["Months_on_book"] / 12).replace(0, np.nan),
    ).fillna(0)
    featured["Service_Friction_Index"] = (
        featured["Months_Inactive_12_mon"] + featured["Contacts_Count_12_mon"]
    )
    return featured


def build_training_frame(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    cleaned = clean_dataset(df)
    missing = [column for column in FEATURE_COLUMNS + [TARGET_COLUMN] if column not in cleaned.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    featured = add_engineered_features(cleaned)
    feature_columns = FEATURE_COLUMNS + ENGINEERED_NUMERIC_FEATURES
    x = featured[feature_columns]
    y = (featured[TARGET_COLUMN] == POSITIVE_CLASS_LABEL).astype(int)
    return x, y


def build_prediction_frame(payload: dict) -> pd.DataFrame:
    df = pd.DataFrame(
        [{PREDICTION_PAYLOAD_RENAME_MAP[key]: value for key, value in payload.items()}]
    )
    return add_engineered_features(df)[FEATURE_COLUMNS + ENGINEERED_NUMERIC_FEATURES]


def keep_dataset_columns(df: pd.DataFrame) -> pd.DataFrame:
    columns = [CLIENT_ID_COLUMN, TARGET_COLUMN, *FEATURE_COLUMNS]
    return clean_dataset(df)[columns]
