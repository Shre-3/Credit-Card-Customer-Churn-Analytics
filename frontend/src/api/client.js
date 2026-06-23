import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "",
});

export async function fetchEdaSummary() {
  const response = await api.get("/api/eda/summary");
  return response.data;
}

export async function fetchModelMetrics() {
  const response = await api.get("/api/model/metrics");
  return response.data;
}

export async function fetchCustomers(churnedOnly = false) {
  const response = await api.get("/api/customers", {
    params: { limit: 100, churned_only: churnedOnly },
  });
  return response.data;
}

export async function predictChurn(payload) {
  const response = await api.post("/api/predictions", payload);
  return response.data;
}

export async function fetchBusinessImpact(saveRate = 0.25, revenuePerCustomer = 450) {
  const response = await api.get("/api/business-impact", {
    params: { save_rate: saveRate, revenue_per_customer: revenuePerCustomer },
  });
  return response.data;
}
