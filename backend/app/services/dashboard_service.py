import json
from pathlib import Path

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.customer_mapper import records_to_dataframe
from app.models.customer import CustomerRecord
from app.schemas.dashboard import BusinessImpact, EdaSummary, MetricCard, ModelMetrics


def _records_to_frame(db: Session) -> pd.DataFrame:
    records = db.scalars(select(CustomerRecord)).all()
    return records_to_dataframe(records)


def _churn_by_category(df: pd.DataFrame, column: str) -> list[dict[str, float | int | str]]:
    grouped = (
        df.assign(churned=df["attrition_flag"].eq("Attrited Customer").astype(int))
        .groupby(column, dropna=False)
        .agg(customers=("client_id", "count"), churn_rate=("churned", "mean"))
        .reset_index()
        .sort_values("churn_rate", ascending=False)
    )
    return [
        {
            "segment": str(row[column]),
            "customers": int(row["customers"]),
            "churn_rate": round(float(row["churn_rate"]), 4),
        }
        for _, row in grouped.iterrows()
    ]


def get_eda_summary(db: Session) -> EdaSummary:
    df = _records_to_frame(db)
    if df.empty:
        return EdaSummary(cards=[], churn_by_category={}, numeric_distributions={})

    churned = df["attrition_flag"].eq("Attrited Customer")
    cards = [
        MetricCard(label="Customers", value=int(len(df))),
        MetricCard(
            label="Churn Rate",
            value=f"{float(churned.mean()) * 100:.2f}%",
            detail="Attrited customers / all customers",
        ),
        MetricCard(label="Avg Credit Limit", value=round(float(df["credit_limit"].mean()), 2)),
        MetricCard(label="Avg Transactions", value=round(float(df["total_trans_ct"].mean()), 2)),
    ]

    numeric_columns = ["customer_age", "credit_limit", "total_trans_amt", "total_trans_ct", "avg_utilization_ratio"]
    numeric_distributions = {}
    for column in numeric_columns:
        numeric_distributions[column] = [
            {
                "attrition_flag": str(group),
                "mean": round(float(values[column].mean()), 4),
                "median": round(float(values[column].median()), 4),
            }
            for group, values in df.groupby("attrition_flag")
        ]

    return EdaSummary(
        cards=cards,
        churn_by_category={
            "gender": _churn_by_category(df, "gender"),
            "education_level": _churn_by_category(df, "education_level"),
            "income_category": _churn_by_category(df, "income_category"),
            "card_category": _churn_by_category(df, "card_category"),
        },
        numeric_distributions=numeric_distributions,
    )


def get_model_metrics() -> ModelMetrics:
    settings = get_settings()
    metrics_path = settings.resolve_path(settings.metrics_artifact_path)
    pr_curve_path = settings.resolve_path(settings.pr_curve_artifact_path)
    shap_path = settings.resolve_path(settings.shap_artifact_path)

    metrics = json.loads(metrics_path.read_text(encoding="utf-8")) if metrics_path.exists() else {}
    pr_curve = json.loads(pr_curve_path.read_text(encoding="utf-8")) if pr_curve_path.exists() else []
    shap_summary = json.loads(shap_path.read_text(encoding="utf-8")) if shap_path.exists() else []

    cards = [
        MetricCard(label="F2 Score", value=round(float(metrics.get("f2_score", 0)), 4), detail="Recall-weighted score"),
        MetricCard(label="Average Precision", value=round(float(metrics.get("average_precision", 0)), 4)),
        MetricCard(label="ROC AUC", value=round(float(metrics.get("roc_auc", 0)), 4)),
        MetricCard(label="Decision Threshold", value=round(float(metrics.get("threshold", 0.5)), 4)),
    ]
    return ModelMetrics(cards=cards, precision_recall_curve=pr_curve, feature_importance=shap_summary)


def get_business_impact(db: Session, save_rate: float = 0.25, revenue_per_customer: float = 450.0) -> BusinessImpact:
    df = _records_to_frame(db)
    if df.empty:
        return BusinessImpact(
            total_customers=0,
            high_risk_customers=0,
            average_revenue_at_risk=revenue_per_customer,
            estimated_revenue_at_risk=0,
            estimated_revenue_saved=0,
            assumptions=[],
        )

    high_risk = df[
        (df["months_inactive_12_mon"] >= 3)
        & (df["contacts_count_12_mon"] >= 3)
        & (df["total_trans_ct"] < df["total_trans_ct"].median())
    ]
    revenue_at_risk = len(high_risk) * revenue_per_customer

    return BusinessImpact(
        total_customers=int(len(df)),
        high_risk_customers=int(len(high_risk)),
        average_revenue_at_risk=float(revenue_per_customer),
        estimated_revenue_at_risk=round(float(revenue_at_risk), 2),
        estimated_revenue_saved=round(float(revenue_at_risk * save_rate), 2),
        assumptions=[
            "High-risk proxy: inactive for at least 3 months, contacted at least 3 times, and below-median transaction count.",
            f"Retention intervention save rate: {save_rate:.0%}.",
            f"Average annual revenue at risk per customer: ${revenue_per_customer:,.2f}.",
        ],
    )
