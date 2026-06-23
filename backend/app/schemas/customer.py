from pydantic import BaseModel, Field


class CustomerBase(BaseModel):
    customer_age: int = Field(..., ge=18, le=100)
    gender: str
    dependent_count: int = Field(..., ge=0)
    education_level: str
    marital_status: str
    income_category: str
    card_category: str
    months_on_book: int = Field(..., ge=0)
    total_relationship_count: int = Field(..., ge=0)
    months_inactive_12_mon: int = Field(..., ge=0)
    contacts_count_12_mon: int = Field(..., ge=0)
    credit_limit: float = Field(..., ge=0)
    total_revolving_bal: int = Field(..., ge=0)
    avg_open_to_buy: float = Field(..., ge=0)
    total_amt_chng_q4_q1: float = Field(..., ge=0)
    total_trans_amt: int = Field(..., ge=0)
    total_trans_ct: int = Field(..., ge=0)
    total_ct_chng_q4_q1: float = Field(..., ge=0)
    avg_utilization_ratio: float = Field(..., ge=0, le=1)


class CustomerResponse(CustomerBase):
    client_id: int
    attrition_flag: str
    churned: bool

    model_config = {"from_attributes": True}


class PredictionRequest(CustomerBase):
    pass


class PredictionResponse(BaseModel):
    churn_probability: float
    risk_band: str
    recommended_action: str
    top_drivers: list[dict[str, float | str]]
