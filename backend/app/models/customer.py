from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class CustomerRecord(Base):
    __tablename__ = "customer_records"

    client_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    attrition_flag: Mapped[str] = mapped_column(String(32), index=True)
    customer_age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(8))
    dependent_count: Mapped[int] = mapped_column(Integer)
    education_level: Mapped[str] = mapped_column(String(64))
    marital_status: Mapped[str] = mapped_column(String(32))
    income_category: Mapped[str] = mapped_column(String(64))
    card_category: Mapped[str] = mapped_column(String(32))
    months_on_book: Mapped[int] = mapped_column(Integer)
    total_relationship_count: Mapped[int] = mapped_column(Integer)
    months_inactive_12_mon: Mapped[int] = mapped_column(Integer)
    contacts_count_12_mon: Mapped[int] = mapped_column(Integer)
    credit_limit: Mapped[float] = mapped_column(Float)
    total_revolving_bal: Mapped[int] = mapped_column(Integer)
    avg_open_to_buy: Mapped[float] = mapped_column(Float)
    total_amt_chng_q4_q1: Mapped[float] = mapped_column(Float)
    total_trans_amt: Mapped[int] = mapped_column(Integer)
    total_trans_ct: Mapped[int] = mapped_column(Integer)
    total_ct_chng_q4_q1: Mapped[float] = mapped_column(Float)
    avg_utilization_ratio: Mapped[float] = mapped_column(Float)
