import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import shap
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    average_precision_score,
    fbeta_score,
    precision_recall_curve,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

from ml.constants import CATEGORICAL_FEATURES, ENGINEERED_NUMERIC_FEATURES, NUMERIC_FEATURES
from ml.features import build_training_frame


def build_pipeline(scale_pos_weight: float) -> Pipeline:
    numeric_features = NUMERIC_FEATURES + ENGINEERED_NUMERIC_FEATURES
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                numeric_features,
            ),
            (
                "categorical",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
                    ]
                ),
                CATEGORICAL_FEATURES,
            ),
        ]
    )

    classifier = XGBClassifier(
        n_estimators=350,
        max_depth=4,
        learning_rate=0.04,
        subsample=0.9,
        colsample_bytree=0.85,
        objective="binary:logistic",
        eval_metric="aucpr",
        random_state=42,
        scale_pos_weight=scale_pos_weight,
    )

    return Pipeline(steps=[("preprocessor", preprocessor), ("classifier", classifier)])


def find_best_f2_threshold(y_true: pd.Series, probabilities: np.ndarray) -> tuple[float, float]:
    precision, recall, thresholds = precision_recall_curve(y_true, probabilities)
    if len(thresholds) == 0:
        return 0.5, 0.0

    scores = []
    for threshold in thresholds:
        predictions = (probabilities >= threshold).astype(int)
        scores.append(fbeta_score(y_true, predictions, beta=2, zero_division=0))

    best_index = int(np.argmax(scores))
    return float(thresholds[best_index]), float(scores[best_index])


def serialize_precision_recall_curve(y_true: pd.Series, probabilities: np.ndarray) -> list[dict[str, float]]:
    precision, recall, thresholds = precision_recall_curve(y_true, probabilities)
    curve = []
    for index, precision_value in enumerate(precision):
        curve.append(
            {
                "precision": float(precision_value),
                "recall": float(recall[index]),
                "threshold": float(thresholds[index]) if index < len(thresholds) else 1.0,
            }
        )
    return curve


def compute_shap_summary(pipeline: Pipeline, x_sample: pd.DataFrame) -> list[dict[str, float | str]]:
    preprocessor = pipeline.named_steps["preprocessor"]
    classifier = pipeline.named_steps["classifier"]
    transformed = preprocessor.transform(x_sample)
    feature_names = preprocessor.get_feature_names_out()

    explainer = shap.TreeExplainer(classifier)
    shap_values = explainer.shap_values(transformed)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    importance = np.abs(shap_values).mean(axis=0)
    sorted_indexes = np.argsort(importance)[::-1][:20]
    return [
        {
            "feature": str(feature_names[index]),
            "mean_abs_shap": float(importance[index]),
        }
        for index in sorted_indexes
    ]


def train_churn_model(input_path: Path, artifacts_dir: Path) -> dict[str, float]:
    df = pd.read_csv(input_path)
    x, y = build_training_frame(df)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )
    negative_count = int((y_train == 0).sum())
    positive_count = int((y_train == 1).sum())
    scale_pos_weight = negative_count / max(positive_count, 1)

    pipeline = build_pipeline(scale_pos_weight=scale_pos_weight)
    pipeline.fit(x_train, y_train)

    probabilities = pipeline.predict_proba(x_test)[:, 1]
    threshold, f2 = find_best_f2_threshold(y_test, probabilities)
    predictions = (probabilities >= threshold).astype(int)

    metrics = {
        "f2_score": float(f2),
        "precision": float((predictions[y_test.to_numpy() == 1].sum()) / max(predictions.sum(), 1)),
        "recall": float(((predictions == 1) & (y_test.to_numpy() == 1)).sum() / max((y_test == 1).sum(), 1)),
        "average_precision": float(average_precision_score(y_test, probabilities)),
        "roc_auc": float(roc_auc_score(y_test, probabilities)),
        "threshold": float(threshold),
        "test_size": int(len(y_test)),
        "churn_rate": float(y.mean()),
    }

    artifacts_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "pipeline": pipeline,
            "threshold": threshold,
            "feature_columns": list(x.columns),
        },
        artifacts_dir / "model.joblib",
    )
    (artifacts_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    (artifacts_dir / "precision_recall_curve.json").write_text(
        json.dumps(serialize_precision_recall_curve(y_test, probabilities), indent=2),
        encoding="utf-8",
    )

    shap_sample = x_test.sample(min(500, len(x_test)), random_state=42)
    shap_summary = compute_shap_summary(pipeline, shap_sample)
    (artifacts_dir / "shap_summary.json").write_text(json.dumps(shap_summary, indent=2), encoding="utf-8")
    return metrics
