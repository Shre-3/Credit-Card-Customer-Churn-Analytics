export function MetricCard({ metric }) {
  let value = metric.value;
  if (metric.label === "Churn Rate" && typeof metric.value === "number") {
    value = `${(metric.value * 100).toFixed(2)}%`;
  }
  if (metric.label === "Churn Rate" && typeof metric.value === "string" && !metric.value.includes("%")) {
    value = `${(Number(metric.value) * 100).toFixed(2)}%`;
  }

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <p className="text-sm font-medium text-slate-500">{metric.label}</p>
      <p className="mt-2 text-3xl font-semibold text-slate-950">{value}</p>
      {metric.detail ? <p className="mt-2 text-sm text-slate-500">{metric.detail}</p> : null}
    </div>
  );
}
