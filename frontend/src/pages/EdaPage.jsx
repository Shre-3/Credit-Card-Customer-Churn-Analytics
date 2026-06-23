import { useEffect, useState } from "react";
import Plot from "react-plotly.js";

import { fetchEdaSummary } from "../api/client";
import { MetricCard } from "../components/MetricCard";
import { plotConfig, plotLayout } from "../utils/chart";

export function EdaPage() {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchEdaSummary().then(setSummary).catch(() => setError("Unable to load EDA summary. Seed the database first."));
  }, []);

  if (error) {
    return <div className="rounded-2xl bg-red-50 p-6 text-red-700">{error}</div>;
  }

  if (!summary) {
    return <div className="rounded-2xl bg-white p-6 text-slate-500 shadow-sm">Loading EDA...</div>;
  }

  const incomeData = (summary.churn_by_category.income_category ?? [])
    .map((item) => ({
      ...item,
      segment: item.segment === "Unknown" ? "Unknown / Not disclosed" : item.segment,
    }))
    .reverse();
  const transactionDistribution = summary.numeric_distributions.total_trans_ct ?? [];
  const attritionColors = {
    "Attrited Customer": "#ef4444",
    "Existing Customer": "#b7e4c7",
  };

  return (
    <section className="space-y-8">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.25em] text-cyan-600">EDA Page</p>
        <h2 className="mt-2 text-3xl font-bold">Who is leaving, and how are they behaving?</h2>
        <p className="mt-3 max-w-3xl text-slate-600">
          Explore churn patterns across customer segments and engagement indicators before modeling.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {summary.cards.map((metric) => (
          <MetricCard key={metric.label} metric={metric} />
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h3 className="text-lg font-semibold">Churn Rate by Income Category</h3>
          <Plot
            config={plotConfig}
            data={[
              {
                x: incomeData.map((item) => item.churn_rate),
                y: incomeData.map((item) => item.segment),
                type: "bar",
                orientation: "h",
                marker: { color: "#0891b2" },
                text: incomeData.map((item) => `${Math.round(item.churn_rate * 100)}%`),
                textposition: "auto",
              },
            ]}
            layout={{
              ...plotLayout,
              margin: { t: 30, r: 30, b: 50, l: 160 },
              xaxis: { tickformat: ".0%", title: { text: "Churn rate" } },
              yaxis: { automargin: true },
            }}
            style={{ height: 380, width: "100%" }}
          />
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h3 className="text-lg font-semibold">Transaction Count by Attrition</h3>
          <Plot
            config={plotConfig}
            data={[
              {
                x: transactionDistribution.map((item) => item.attrition_flag),
                y: transactionDistribution.map((item) => item.mean),
                type: "bar",
                marker: { color: transactionDistribution.map((item) => attritionColors[item.attrition_flag] ?? "#64748b") },
              },
            ]}
            layout={{ ...plotLayout, yaxis: { title: { text: "Mean transaction count" } } }}
            style={{ height: 380, width: "100%" }}
          />
        </div>
      </div>
    </section>
  );
}
