import { useEffect, useState } from "react";
import Plot from "react-plotly.js";

import { fetchBusinessImpact } from "../api/client";
import { MetricCard } from "../components/MetricCard";
import { plotConfig, plotLayout } from "../utils/chart";

export function BusinessImpactPage() {
  const [saveRate, setSaveRate] = useState(0.25);
  const [revenuePerCustomer, setRevenuePerCustomer] = useState(450);
  const [impact, setImpact] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchBusinessImpact(saveRate, revenuePerCustomer)
      .then(setImpact)
      .catch(() => setError("Unable to load business impact. Seed the database first."));
  }, [saveRate, revenuePerCustomer]);

  if (error) {
    return <div className="rounded-2xl bg-red-50 p-6 text-red-700">{error}</div>;
  }

  if (!impact) {
    return <div className="rounded-2xl bg-white p-6 text-slate-500 shadow-sm">Loading business impact...</div>;
  }

  const cards = [
    { label: "Total Customers", value: impact.total_customers },
    { label: "High-Risk Customers", value: impact.high_risk_customers },
    { label: "Revenue at Risk", value: `$${impact.estimated_revenue_at_risk.toLocaleString()}` },
    { label: "Estimated Saved", value: `$${impact.estimated_revenue_saved.toLocaleString()}` },
  ];

  return (
    <section className="space-y-8">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.25em] text-cyan-600">Business Impact Page</p>
        <h2 className="mt-2 text-3xl font-bold">Translate churn risk into retention value</h2>
        <p className="mt-3 max-w-3xl text-slate-600">
          Estimate potential revenue protected by targeted outreach to customers with high-risk engagement patterns.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {cards.map((metric) => (
          <MetricCard key={metric.label} metric={metric} />
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-[0.8fr_1.2fr]">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="text-lg font-semibold">Scenario Assumptions</h3>
          <label className="mt-5 block space-y-2 text-sm font-medium text-slate-700">
            <span>Intervention Save Rate: {Math.round(saveRate * 100)}%</span>
            <input
              className="w-full accent-cyan-600"
              max="1"
              min="0"
              onChange={(event) => setSaveRate(Number(event.target.value))}
              step="0.05"
              type="range"
              value={saveRate}
            />
          </label>
          <label className="mt-5 block space-y-2 text-sm font-medium text-slate-700">
            <span>Annual Revenue at Risk per Customer ($)</span>
            <input
              className="w-full rounded-xl border border-slate-300 px-3 py-2 outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-100"
              min="0"
              onChange={(event) => setRevenuePerCustomer(Number(event.target.value))}
              type="number"
              value={revenuePerCustomer}
            />
          </label>
          <ul className="mt-6 space-y-3 text-sm text-slate-600">
            {impact.assumptions.map((assumption) => (
              <li className="rounded-xl bg-slate-50 p-3" key={assumption}>
                {assumption}
              </li>
            ))}
          </ul>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h3 className="text-lg font-semibold">Revenue Scenario</h3>
          <Plot
            config={plotConfig}
            data={[
              {
                x: ["Revenue at Risk", "Estimated Saved"],
                y: [impact.estimated_revenue_at_risk, impact.estimated_revenue_saved],
                type: "bar",
                marker: { color: ["#ef4444", "#10b981"] },
              },
            ]}
            layout={{ ...plotLayout, yaxis: { title: { text: "Revenue ($)" } } }}
            style={{ height: 420, width: "100%" }}
          />
        </div>
      </div>
    </section>
  );
}
