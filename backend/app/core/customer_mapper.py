from sqlalchemy import inspect

import pandas as pd

from app.models.customer import CustomerRecord
from app.schemas.customer import CustomerResponse
from ml.constants import POSITIVE_CLASS_LABEL


def record_to_customer_response(record: CustomerRecord) -> CustomerResponse:
    data = {column.key: getattr(record, column.key) for column in inspect(CustomerRecord).mapper.column_attrs}
    return CustomerResponse(
        **data,
        churned=record.attrition_flag == POSITIVE_CLASS_LABEL,
    )


def records_to_dataframe(records: list[CustomerRecord]) -> pd.DataFrame:
    if not records:
        return pd.DataFrame()

    rows = [
        {column.key: getattr(record, column.key) for column in inspect(CustomerRecord).mapper.column_attrs}
        for record in records
    ]
    frame = pd.DataFrame(rows)
    frame["churned"] = frame["attrition_flag"].eq(POSITIVE_CLASS_LABEL)
    return frame
