from pydantic import BaseModel


class MetricCard(BaseModel):
    label: str
    value: float | int | str
    detail: str | None = None


class EdaSummary(BaseModel):
    cards: list[MetricCard]
    churn_by_category: dict[str, list[dict[str, float | int | str]]]
    numeric_distributions: dict[str, list[dict[str, float | int | str]]]


class ModelMetrics(BaseModel):
    cards: list[MetricCard]
    precision_recall_curve: list[dict[str, float]]
    feature_importance: list[dict[str, float | str]]


class BusinessImpact(BaseModel):
    total_customers: int
    high_risk_customers: int
    average_revenue_at_risk: float
    estimated_revenue_at_risk: float
    estimated_revenue_saved: float
    assumptions: list[str]
