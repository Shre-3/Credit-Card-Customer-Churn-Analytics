from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.customer import CustomerResponse, PredictionRequest, PredictionResponse
from app.schemas.dashboard import BusinessImpact, EdaSummary, ModelMetrics
from app.services.customer_service import list_customers
from app.services.dashboard_service import get_business_impact, get_eda_summary, get_model_metrics
from app.services.model_service import model_service

router = APIRouter(prefix="/api")


@router.get("/eda/summary", response_model=EdaSummary)
def eda_summary(db: Session = Depends(get_db)) -> EdaSummary:
    return get_eda_summary(db)


@router.get("/model/metrics", response_model=ModelMetrics)
def model_metrics() -> ModelMetrics:
    return get_model_metrics()


@router.get("/customers", response_model=list[CustomerResponse])
def customers(
    limit: int = Query(default=100, ge=1, le=1000),
    churned_only: bool = False,
    db: Session = Depends(get_db),
) -> list[CustomerResponse]:
    return list_customers(db, limit=limit, churned_only=churned_only)


@router.post("/predictions", response_model=PredictionResponse)
def predict_churn(request: PredictionRequest) -> PredictionResponse:
    try:
        return model_service.predict(request)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.get("/business-impact", response_model=BusinessImpact)
def business_impact(
    save_rate: float = Query(default=0.25, ge=0, le=1),
    revenue_per_customer: float = Query(default=450.0, ge=0),
    db: Session = Depends(get_db),
) -> BusinessImpact:
    return get_business_impact(db, save_rate=save_rate, revenue_per_customer=revenue_per_customer)
