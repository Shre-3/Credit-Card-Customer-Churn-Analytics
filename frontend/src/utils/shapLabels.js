const featureLabels = {
  Total_Trans_Ct: "Transaction Count (12 mo)",
  Total_Trans_Amt: "Transaction Amount (12 mo)",
  Total_Revolving_Bal: "Revolving Balance",
  Average_Transaction_Value: "Avg Transaction Value",
  Total_Ct_Chng_Q4_Q1: "Transaction Count Change (Q4 vs Q1)",
  Total_Amt_Chng_Q4_Q1: "Transaction Amount Change (Q4 vs Q1)",
  Total_Relationship_Count: "Bank Relationships",
  Months_Inactive_12_mon: "Inactive Months (12 mo)",
  Service_Friction_Index: "Service Friction Index",
  Customer_Age: "Customer Age",
  Credit_Limit: "Credit Limit",
  Relationship_Depth_Per_Year: "Relationships per Year",
  Avg_Utilization_Ratio: "Credit Utilization Ratio",
  Contacts_Count_12_mon: "Customer Contacts (12 mo)",
  Avg_Open_To_Buy: "Open-to-Buy Amount",
  Months_on_book: "Months With Bank",
  Dependent_count: "Number of Dependents",
  Balance_To_Limit_Ratio: "Balance-to-Limit Ratio",
  Gender_F: "Gender: Female",
  Gender_M: "Gender: Male",
  Marital_Status_Married: "Marital Status: Married",
  Marital_Status_Single: "Marital Status: Single",
  Marital_Status_Divorced: "Marital Status: Divorced",
  Marital_Status_Unknown: "Marital Status: Unknown",
};

export function formatShapFeatureName(feature) {
  const raw = feature.replace(/^numeric__/, "").replace(/^categorical__/, "");

  if (featureLabels[raw]) {
    return featureLabels[raw];
  }

  return raw.replace(/_/g, " ");
}
