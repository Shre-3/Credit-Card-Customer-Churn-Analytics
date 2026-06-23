TARGET_COLUMN = "Attrition_Flag"
CLIENT_ID_COLUMN = "CLIENTNUM"
POSITIVE_CLASS_LABEL = "Attrited Customer"

LEAKAGE_COLUMNS = [
    "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1",
    "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2",
]

FEATURE_COLUMNS = [
    "Customer_Age",
    "Gender",
    "Dependent_count",
    "Education_Level",
    "Marital_Status",
    "Income_Category",
    "Card_Category",
    "Months_on_book",
    "Total_Relationship_Count",
    "Months_Inactive_12_mon",
    "Contacts_Count_12_mon",
    "Credit_Limit",
    "Total_Revolving_Bal",
    "Avg_Open_To_Buy",
    "Total_Amt_Chng_Q4_Q1",
    "Total_Trans_Amt",
    "Total_Trans_Ct",
    "Total_Ct_Chng_Q4_Q1",
    "Avg_Utilization_Ratio",
]

CATEGORICAL_FEATURES = [
    "Gender",
    "Education_Level",
    "Marital_Status",
    "Income_Category",
    "Card_Category",
]

NUMERIC_FEATURES = [column for column in FEATURE_COLUMNS if column not in CATEGORICAL_FEATURES]

ENGINEERED_NUMERIC_FEATURES = [
    "Balance_To_Limit_Ratio",
    "Average_Transaction_Value",
    "Relationship_Depth_Per_Year",
    "Service_Friction_Index",
]

CSV_TO_SNAKE_COLUMN_MAP = {
    CLIENT_ID_COLUMN: "client_id",
    TARGET_COLUMN: "attrition_flag",
    "Customer_Age": "customer_age",
    "Gender": "gender",
    "Dependent_count": "dependent_count",
    "Education_Level": "education_level",
    "Marital_Status": "marital_status",
    "Income_Category": "income_category",
    "Card_Category": "card_category",
    "Months_on_book": "months_on_book",
    "Total_Relationship_Count": "total_relationship_count",
    "Months_Inactive_12_mon": "months_inactive_12_mon",
    "Contacts_Count_12_mon": "contacts_count_12_mon",
    "Credit_Limit": "credit_limit",
    "Total_Revolving_Bal": "total_revolving_bal",
    "Avg_Open_To_Buy": "avg_open_to_buy",
    "Total_Amt_Chng_Q4_Q1": "total_amt_chng_q4_q1",
    "Total_Trans_Amt": "total_trans_amt",
    "Total_Trans_Ct": "total_trans_ct",
    "Total_Ct_Chng_Q4_Q1": "total_ct_chng_q4_q1",
    "Avg_Utilization_Ratio": "avg_utilization_ratio",
}

PREDICTION_PAYLOAD_RENAME_MAP = {
    snake: csv
    for csv, snake in CSV_TO_SNAKE_COLUMN_MAP.items()
    if csv not in {CLIENT_ID_COLUMN, TARGET_COLUMN}
}
