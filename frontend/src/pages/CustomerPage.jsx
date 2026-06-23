import { useEffect, useState } from "react";

import { fetchCustomers } from "../api/client";

export function CustomerPage() {
  const [customers, setCustomers] = useState([]);
  const [churnedOnly, setChurnedOnly] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCustomers(churnedOnly)
      .then(setCustomers)
      .catch(() => setError("Unable to load customers. Seed the database first."));
  }, [churnedOnly]);

  if (error) {
    return <div className="rounded-2xl bg-red-50 p-6 text-red-700">{error}</div>;
  }

  return (
    <section className="space-y-8">
      <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-cyan-600">Customer Page</p>
          <h2 className="mt-2 text-3xl font-bold">Customer-level churn exploration</h2>
          <p className="mt-3 max-w-3xl text-slate-600">
            Review individual customer records and compare known attrited customers against current portfolio behavior.
          </p>
        </div>
        <label className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm shadow-sm">
          <input
            checked={churnedOnly}
            className="h-4 w-4 accent-cyan-600"
            onChange={(event) => setChurnedOnly(event.target.checked)}
            type="checkbox"
          />
          Show churned customers only
        </label>
      </div>

      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200 text-sm">
            <thead className="bg-slate-100 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-4 py-3">Client ID</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Age</th>
                <th className="px-4 py-3">Income</th>
                <th className="px-4 py-3">Card</th>
                <th className="px-4 py-3">Inactive Months</th>
                <th className="px-4 py-3">Contacts</th>
                <th className="px-4 py-3">Transactions</th>
                <th className="px-4 py-3">Utilization</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {customers.map((customer) => (
                <tr key={customer.client_id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-medium text-slate-950">{customer.client_id}</td>
                  <td className="px-4 py-3">
                    <span
                      className={`rounded-full px-3 py-1 text-xs font-semibold ${
                        customer.churned ? "bg-red-100 text-red-700" : "bg-emerald-100 text-emerald-700"
                      }`}
                    >
                      {customer.attrition_flag}
                    </span>
                  </td>
                  <td className="px-4 py-3">{customer.customer_age}</td>
                  <td className="px-4 py-3">{customer.income_category}</td>
                  <td className="px-4 py-3">{customer.card_category}</td>
                  <td className="px-4 py-3">{customer.months_inactive_12_mon}</td>
                  <td className="px-4 py-3">{customer.contacts_count_12_mon}</td>
                  <td className="px-4 py-3">{customer.total_trans_ct}</td>
                  <td className="px-4 py-3">{Math.round(customer.avg_utilization_ratio * 100)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
