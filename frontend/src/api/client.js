import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api/v1";

export const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("finsight_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("finsight_token");
      if (!window.location.pathname.startsWith("/login") && !window.location.pathname.startsWith("/register")) {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

// Auth
export const register = (payload) => api.post("/auth/register", payload);
export const login = (payload) => api.post("/auth/login", payload);
export const getMe = () => api.get("/auth/me");

// Companies
export const createCompany = (payload) => api.post("/companies", payload);
export const listCompanies = () => api.get("/companies");

// Statements
export const bulkUploadStatements = (companyId, statements) =>
  api.post(`/statements/${companyId}/bulk`, { statements });
export const listStatements = (companyId) => api.get(`/statements/${companyId}`);

// Analysis
export const analyzeCompany = (companyId) => api.get(`/analysis/${companyId}`);

// Predictions
export const predictCashflow = (companyId, horizon = 3) =>
  api.post("/predictions", { company_id: companyId, horizon });

// Anomalies
export const detectAnomalies = (companyId) => api.get(`/anomalies/${companyId}`);

// Reports
export const getReport = (companyId) => api.get(`/reports/${companyId}`);
export const downloadReportPdf = (companyId) =>
  api.get(`/reports/${companyId}/pdf`, { responseType: "blob" });


// ---------- Advanced endpoints ----------
export const uploadExcel = (companyId, file) => {
  const form = new FormData();
  form.append("file", file);
  return api.post(`/advanced/upload/excel/${companyId}`, form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const advancedPredict = (companyId, horizon = 3) =>
  api.get(`/advanced/predict/${companyId}?horizon=${horizon}`);

export const getTrends = (companyId) => api.get(`/advanced/trends/${companyId}`);

export const getZScore = (companyId, threshold = 2.0) =>
  api.get(`/advanced/zscore/${companyId}?threshold=${threshold}`);

export const getLimeExplanation = (companyId) =>
  api.get(`/advanced/lime/${companyId}`);

export const getTextExplanation = (companyId) =>
  api.get(`/advanced/explanation/${companyId}`);

export const downloadExcelReport = (companyId) =>
  api.get(`/advanced/report/${companyId}/excel`, { responseType: "blob" });
