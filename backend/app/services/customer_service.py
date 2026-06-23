from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.customer_mapper import record_to_customer_response

from app.models.customer import CustomerRecord
from app.schemas.customer import CustomerResponse


def list_customers(db: Session, limit: int = 100, churned_only: bool = False) -> list[CustomerResponse]:
    statement = select(CustomerRecord).limit(limit)
    if churned_only:
        statement = select(CustomerRecord).where(CustomerRecord.attrition_flag == "Attrited Customer").limit(limit)
    records = db.scalars(statement).all()
    return [record_to_customer_response(record) for record in records]
