import { useEffect, useState } from "react";
import Plot from "react-plotly.js";

import { fetchModelMetrics } from "../api/client";
import { MetricCard } from "../components/MetricCard";
import { plotConfig, plotLayout } from "../utils/chart";
import { formatShapFeatureName } from "../utils/shapLabels";

export function ModelPage() {
  const [metrics, setMetrics] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchModelMetrics()
      .then(setMetrics)
      .catch(() => setError("Unable to load model metrics. Train the model first."));
  }, []);

  if (error) {
    return <div className="rounded-2xl bg-red-50 p-6 text-red-700">{error}</div>;
  }

  if (!metrics) {
    return <div className="rounded-2xl bg-white p-6 text-slate-500 shadow-sm">Loading model metrics...</div>;
  }

  const topFeatures = metrics.feature_importance.slice(0, 12).reverse();

  return (
    <section className="space-y-8">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.25em] text-cyan-600">Model Page</p>
        <h2 className="mt-2 text-3xl font-bold">XGBoost churn model performance</h2>
        <p className="mt-3 max-w-3xl text-slate-600">
          The model is optimized for churn detection using F2-score because missing likely churners is more costly than
          sending a few extra retention offers.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {metrics.cards.map((metric) => (
          <MetricCard key={metric.label} metric={metric} />
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h3 className="text-lg font-semibold">Precision-Recall Curve</h3>
          <Plot
            config={plotConfig}
            data={[
              {
                x: metrics.precision_recall_curve.map((point) => point.recall),
                y: metrics.precision_recall_curve.map((point) => point.precision),
                type: "scatter",
                mode: "lines",
                line: { color: "#0891b2", width: 3 },
              },
            ]}
            layout={{ ...plotLayout, xaxis: { title: { text: "Recall" } }, yaxis: { title: { text: "Precision" } } }}
            style={{ height: 380, width: "100%" }}
          />
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h3 className="text-lg font-semibold">Top SHAP Drivers</h3>
          <p className="mt-1 text-sm text-slate-500">Features with the strongest influence on churn predictions.</p>
          <Plot
            config={plotConfig}
            data={[
              {
                x: topFeatures.map((item) => item.mean_abs_shap),
                y: topFeatures.map((item) => formatShapFeatureName(item.feature)),
                type: "bar",
                orientation: "h",
                marker: { color: "#0f172a" },
                hovertemplate: "%{y}<br>SHAP impact: %{x:.3f}<extra></extra>",
              },
            ]}
            layout={{
              ...plotLayout,
              margin: { t: 20, r: 24, b: 48, l: 200 },
              xaxis: { title: { text: "Mean absolute SHAP value" } },
              yaxis: { automargin: true, tickfont: { size: 12 } },
            }}
            style={{ height: 460, width: "100%" }}
          />
        </div>
      </div>
    </section>
  );
}
