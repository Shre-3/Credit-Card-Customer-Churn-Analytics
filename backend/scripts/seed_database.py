import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.session import Base, SessionLocal, engine
from app.models.customer import CustomerRecord
from ml.constants import CSV_TO_SNAKE_COLUMN_MAP
from ml.features import keep_dataset_columns


STRING_FIELDS = {
    "attrition_flag",
    "gender",
    "education_level",
    "marital_status",
    "income_category",
    "card_category",
}
FLOAT_FIELDS = {
    "credit_limit",
    "avg_open_to_buy",
    "total_amt_chng_q4_q1",
    "total_ct_chng_q4_q1",
    "avg_utilization_ratio",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed PostgreSQL with credit card customer records.")
    parser.add_argument("--input", type=Path, required=True, help="Path to BankChurners.csv")
    return parser.parse_args()


def text_value(value: object) -> str:
    if pd.isna(value):
        return "Unknown"
    return str(value)


def coerce_column_value(snake: str, value: object) -> object:
    if snake in STRING_FIELDS:
        return text_value(value)
    if snake in FLOAT_FIELDS:
        return float(value)
    return int(value)


def build_record(row: pd.Series) -> CustomerRecord:
    return CustomerRecord(
        **{
            snake: coerce_column_value(snake, row[csv_column])
            for csv_column, snake in CSV_TO_SNAKE_COLUMN_MAP.items()
        }
    )


def main() -> None:
    args = parse_args()
    df = keep_dataset_columns(pd.read_csv(args.input))

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        for _, row in df.iterrows():
            db.merge(build_record(row))
        db.commit()

    print(f"Seeded {len(df)} customer records")


if __name__ == "__main__":
    main()
