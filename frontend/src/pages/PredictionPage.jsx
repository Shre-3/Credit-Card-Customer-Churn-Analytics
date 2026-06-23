import { useState } from "react";

import { predictChurn } from "../api/client";
import { RiskBadge } from "../components/RiskBadge";
import { formatShapFeatureName } from "../utils/shapLabels";

const initialPayload = {
  customer_age: 45,
  gender: "F",
  dependent_count: 3,
  education_level: "Graduate",
  marital_status: "Married",
  income_category: "$40K - $60K",
  card_category: "Blue",
  months_on_book: 36,
  total_relationship_count: 3,
  months_inactive_12_mon: 3,
  contacts_count_12_mon: 3,
  credit_limit: 12691,
  total_revolving_bal: 777,
  avg_open_to_buy: 11914,
  total_amt_chng_q4_q1: 1.335,
  total_trans_amt: 1144,
  total_trans_ct: 42,
  total_ct_chng_q4_q1: 1.625,
  avg_utilization_ratio: 0.061,
};

const numericFields = new Set([
  "customer_age",
  "dependent_count",
  "months_on_book",
  "total_relationship_count",
  "months_inactive_12_mon",
  "contacts_count_12_mon",
  "credit_limit",
  "total_revolving_bal",
  "avg_open_to_buy",
  "total_amt_chng_q4_q1",
  "total_trans_amt",
  "total_trans_ct",
  "total_ct_chng_q4_q1",
  "avg_utilization_ratio",
]);

const categoryOptions = {
  gender: ["F", "M"],
  education_level: ["Uneducated", "High School", "College", "Graduate", "Post-Graduate", "Doctorate", "Unknown"],
  marital_status: ["Single", "Married", "Divorced", "Unknown"],
  income_category: ["Less than $40K", "$40K - $60K", "$60K - $80K", "$80K - $120K", "$120K +", "Unknown"],
  card_category: ["Blue", "Silver", "Gold", "Platinum"],
};

const fieldLabels = {
  customer_age: "Customer Age",
  gender: "Gender",
  dependent_count: "Number of Dependents",
  education_level: "Education Level",
  marital_status: "Marital Status",
  income_category: "Income Category",
  card_category: "Card Category",
  months_on_book: "Months With the Bank",
  total_relationship_count: "Total Bank Relationships",
  months_inactive_12_mon: "Inactive Months (Last 12)",
  contacts_count_12_mon: "Customer Contacts (Last 12 Months)",
  credit_limit: "Credit Limit",
  total_revolving_bal: "Total Revolving Balance",
  avg_open_to_buy: "Average Open-to-Buy Amount",
  total_amt_chng_q4_q1: "Transaction Amount Change (Q4 vs Q1)",
  total_trans_amt: "Total Transaction Amount (Last 12 Months)",
  total_trans_ct: "Total Transaction Count (Last 12 Months)",
  total_ct_chng_q4_q1: "Transaction Count Change (Q4 vs Q1)",
  avg_utilization_ratio: "Average Credit Utilization Ratio",
};

const fieldOrder = [
  "customer_age",
  "gender",
  "dependent_count",
  "education_level",
  "marital_status",
  "income_category",
  "card_category",
  "months_on_book",
  "total_relationship_count",
  "months_inactive_12_mon",
  "contacts_count_12_mon",
  "credit_limit",
  "total_revolving_bal",
  "avg_open_to_buy",
  "avg_utilization_ratio",
  "total_trans_amt",
  "total_trans_ct",
  "total_amt_chng_q4_q1",
  "total_ct_chng_q4_q1",
];

export function PredictionPage() {
  const [payload, setPayload] = useState(initialPayload);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  function updateField(field, value) {
    setPayload((current) => ({
      ...current,
      [field]: numericFields.has(field) ? Number(value) : value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError(null);
    try {
      setPrediction(await predictChurn(payload));
    } catch {
      setError("Prediction failed. Train the model and make sure the API is running.");
    }
  }

  return (
    <section className="space-y-8">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.25em] text-cyan-600">Prediction Page</p>
        <h2 className="mt-2 text-3xl font-bold">Score a customer in real time</h2>
        <p className="mt-3 max-w-3xl text-slate-600">
          Enter a customer profile to receive churn probability, risk band, retention recommendation, and top model
          drivers.
        </p>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.4fr_0.8fr]">
        <form className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm" onSubmit={handleSubmit}>
          <div className="grid gap-4 md:grid-cols-2">
            {fieldOrder.map((field) => (
              <label className="space-y-2 text-sm font-medium text-slate-700" key={field}>
                <span>{fieldLabels[field]}</span>
                {categoryOptions[field] ? (
                  <select
                    className="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-100"
                    onChange={(event) => updateField(field, event.target.value)}
                    value={payload[field]}
                  >
                    {categoryOptions[field].map((option) => (
                      <option key={option} value={option}>
                        {option}
                      </option>
                    ))}
                  </select>
                ) : (
                  <input
                    className="w-full rounded-xl border border-slate-300 px-3 py-2 outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-100"
                    onChange={(event) => updateField(field, event.target.value)}
                    step="any"
                    type={numericFields.has(field) ? "number" : "text"}
                    value={payload[field]}
                  />
                )}
              </label>
            ))}
          </div>
          <button
            className="mt-6 rounded-xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-cyan-700"
            type="submit"
          >
            Predict Churn Risk
          </button>
        </form>

        <aside className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold">Prediction Result</h3>
          {error ? <p className="mt-4 rounded-xl bg-red-50 p-4 text-sm text-red-700">{error}</p> : null}
          {prediction ? (
            <div className="mt-6 space-y-5">
              <div>
                <p className="text-sm text-slate-500">Churn Probability</p>
                <p className="mt-1 text-5xl font-bold text-slate-950">
                  {Math.round(prediction.churn_probability * 100)}%
                </p>
              </div>
              <RiskBadge risk={prediction.risk_band} />
              <p className="rounded-xl bg-cyan-50 p-4 text-sm text-cyan-900">{prediction.recommended_action}</p>
              <div>
                <p className="text-sm font-semibold text-slate-700">Top global SHAP drivers</p>
                <ul className="mt-3 space-y-2 text-sm text-slate-600">
                  {prediction.top_drivers.map((driver) => (
                    <li className="flex justify-between gap-4" key={driver.feature}>
                      <span>{formatShapFeatureName(driver.feature)}</span>
                      <span className="font-medium">{driver.mean_abs_shap.toFixed(3)}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ) : (
            <p className="mt-4 text-sm text-slate-500">Run a prediction to see risk output.</p>
          )}
        </aside>
      </div>
    </section>
  );
}
