"""Bootstrap script - writes all FinSight AI frontend files."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "frontend"

FILES = {}

# ---------- index.html ----------
FILES["index.html"] = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>FinSight AI - Intelligent Financial Analytics</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
'''

# ---------- package.json ----------
FILES["package.json"] = '''{
  "name": "finsight-ai-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "axios": "^1.7.7",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.26.2",
    "recharts": "^2.12.7"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.2",
    "vite": "^5.4.8"
  }
}
'''

# ---------- vite.config.js ----------
FILES["vite.config.js"] = '''import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
});
'''

# ---------- .gitignore ----------
FILES[".gitignore"] = '''node_modules
dist
.vite
*.local
.env
'''

# ---------- public/favicon.svg ----------
FILES["public/favicon.svg"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="6" fill="#2563eb"/>
  <text x="16" y="22" font-family="Arial" font-size="16" font-weight="bold" fill="white" text-anchor="middle">F</text>
</svg>
'''

# ---------- src/main.jsx ----------
FILES["src/main.jsx"] = '''import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import App from "./App";
import { AuthProvider } from "./context/AuthContext";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
'''

# ---------- src/index.css ----------
FILES["src/index.css"] = '''
:root {
  --bg: #0f172a;
  --surface: #ffffff;
  --primary: #2563eb;
  --primary-hover: #1d4ed8;
  --success: #16a34a;
  --warning: #f59e0b;
  --danger: #dc2626;
  --text: #0f172a;
  --text-muted: #64748b;
  --border: #e2e8f0;
}

* { box-sizing: border-box; }
html, body, #root { height: 100%; }
body {
  margin: 0;
  font-family: -apple-system, "Segoe UI", Roboto, "Inter", sans-serif;
  background: #f8fafc;
  color: var(--text);
}
a { color: var(--primary); text-decoration: none; }
a:hover { text-decoration: underline; }

.app-shell { display: flex; min-height: 100vh; }

.sidebar {
  width: 240px;
  background: var(--bg);
  color: #cbd5e1;
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex-shrink: 0;
}
.sidebar .brand {
  color: #fff;
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 24px;
}
.sidebar .brand span { color: #60a5fa; }
.sidebar a {
  color: #cbd5e1;
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 14px;
  text-decoration: none;
  transition: background 0.15s;
}
.sidebar a:hover { background: #1e293b; color: #fff; text-decoration: none; }
.sidebar a.active { background: var(--primary); color: #fff; }

.main { flex: 1; display: flex; flex-direction: column; min-width: 0; }

.topbar {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: #fff;
  border-bottom: 1px solid var(--border);
}
.topbar .title { font-weight: 600; }
.topbar .actions { display: flex; gap: 12px; align-items: center; }

.content { padding: 24px; max-width: 1200px; width: 100%; margin: 0 auto; }

.card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid var(--border);
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
  margin-bottom: 16px;
}

.grid { display: grid; gap: 16px; }
.grid-2 { grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }
.grid-3 { grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }
.grid-4 { grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); }

.stat { display: flex; flex-direction: column; gap: 4px; }
.stat .label {
  color: var(--text-muted);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}
.stat .value { font-size: 24px; font-weight: 700; }

button, .btn {
  background: var(--primary);
  color: #fff;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background 0.15s;
  font-family: inherit;
}
button:hover:not(:disabled), .btn:hover { background: var(--primary-hover); }
button:disabled { opacity: 0.55; cursor: not-allowed; }
.btn-danger { background: var(--danger); }
.btn-success { background: var(--success); }

input, textarea, select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  background: #fff;
}
input:focus, textarea:focus, select:focus {
  outline: 2px solid var(--primary);
  outline-offset: 1px;
}
label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 6px; color: #334155; }
.form-row { margin-bottom: 14px; }

table { width: 100%; border-collapse: collapse; font-size: 14px; }
th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid var(--border); }
th {
  color: var(--text-muted);
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}
.badge.low { background: #dcfce7; color: #166534; }
.badge.medium { background: #fef3c7; color: #92400e; }
.badge.high { background: #fee2e2; color: #991b1b; }

.auth-shell {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #0f172a, #1e293b);
  padding: 20px;
}
.auth-card {
  width: 100%;
  max-width: 420px;
  background: #fff;
  padding: 32px;
  border-radius: 14px;
  box-shadow: 0 12px 40px rgba(15, 23, 42, 0.25);
}
.auth-card h1 { margin: 0 0 6px; font-size: 22px; }
.auth-card p.muted { color: var(--text-muted); margin: 0 0 24px; font-size: 14px; }

.error {
  background: #fee2e2;
  color: #991b1b;
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 13px;
  margin-bottom: 12px;
}
.success {
  background: #dcfce7;
  color: #166534;
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 13px;
  margin-bottom: 12px;
}

.recommendation {
  padding: 12px 16px;
  background: #eff6ff;
  border-left: 3px solid var(--primary);
  border-radius: 6px;
  margin-bottom: 8px;
  font-size: 14px;
}

.muted { color: var(--text-muted); }
h2.page-title { margin: 0 0 20px; font-size: 22px; }
'''

# ---------- src/api/client.js ----------
FILES["src/api/client.js"] = '''import axios from "axios";

export const api = axios.create({
  baseURL: "/api/v1",
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
'''

# ---------- src/context/AuthContext.jsx ----------
FILES["src/context/AuthContext.jsx"] = '''import { createContext, useContext, useEffect, useState } from "react";

import { getMe, login as apiLogin, register as apiRegister } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadUser = async () => {
    const token = localStorage.getItem("finsight_token");
    if (!token) {
      setLoading(false);
      return;
    }
    try {
      const { data } = await getMe();
      setUser(data);
    } catch {
      localStorage.removeItem("finsight_token");
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUser();
  }, []);

  const login = async (payload) => {
    const { data } = await apiLogin(payload);
    localStorage.setItem("finsight_token", data.access_token);
    await loadUser();
  };

  const register = async (payload) => {
    const { data } = await apiRegister(payload);
    localStorage.setItem("finsight_token", data.access_token);
    await loadUser();
  };

  const logout = () => {
    localStorage.removeItem("finsight_token");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
'''

# ---------- src/components/ProtectedRoute.jsx ----------
FILES["src/components/ProtectedRoute.jsx"] = '''import { Navigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div style={{ padding: 40, textAlign: "center" }}>
        Loading…
      </div>
    );
  }
  if (!user) return <Navigate to="/login" replace />;
  return children;
}
'''

# ---------- src/components/Layout.jsx ----------
FILES["src/components/Layout.jsx"] = '''import { NavLink, Outlet, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

const links = [
  { to: "/dashboard", label: "📊 Dashboard" },
  { to: "/upload", label: "📁 Upload Data" },
  { to: "/analysis", label: "📈 Analysis" },
  { to: "/predictions", label: "🔮 Predictions" },
  { to: "/anomalies", label: "⚠️  Anomalies" },
  { to: "/reports", label: "📄 Reports" },
];

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          Fin<span>Sight</span> AI
        </div>
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            {link.label}
          </NavLink>
        ))}
      </aside>

      <div className="main">
        <header className="topbar">
          <div className="title">Intelligent Financial Analytics</div>
          <div className="actions">
            <span style={{ color: "#64748b", fontSize: 14 }}>
              {user?.email}
            </span>
            <button onClick={handleLogout}>Logout</button>
          </div>
        </header>
        <main className="content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
'''

# ---------- src/components/HealthScoreGauge.jsx ----------
FILES["src/components/HealthScoreGauge.jsx"] = '''export default function HealthScoreGauge({ score = 0, riskLevel = "Unknown" }) {
  const radius = 80;
  const circumference = Math.PI * radius;
  const progress = (Math.max(0, Math.min(100, score)) / 100) * circumference;

  const color =
    riskLevel === "Low" ? "#16a34a" : riskLevel === "Medium" ? "#f59e0b" : "#dc2626";

  return (
    <div style={{ textAlign: "center", padding: "10px 0" }}>
      <svg viewBox="0 0 200 120" width="260" height="160">
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke="#e2e8f0"
          strokeWidth="14"
          strokeLinecap="round"
        />
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke={color}
          strokeWidth="14"
          strokeLinecap="round"
          strokeDasharray={`${progress} ${circumference}`}
        />
        <text x="100" y="90" textAnchor="middle" fontSize="28" fontWeight="700" fill="#0f172a">
          {score}
        </text>
        <text x="100" y="110" textAnchor="middle" fontSize="12" fill="#64748b">
          out of 100
        </text>
      </svg>
      <div style={{ marginTop: 6 }}>
        <span className={`badge ${riskLevel.toLowerCase()}`}>{riskLevel} Risk</span>
      </div>
    </div>
  );
}
'''

# ---------- src/components/CashFlowChart.jsx ----------
FILES["src/components/CashFlowChart.jsx"] = '''import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export default function CashFlowChart({ values = [] }) {
  const data = values.map((value, index) => ({
    period: `+${index + 1}`,
    cashflow: value,
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
        <XAxis dataKey="period" />
        <YAxis />
        <Tooltip formatter={(v) => Number(v).toLocaleString()} />
        <Line
          type="monotone"
          dataKey="cashflow"
          stroke="#2563eb"
          strokeWidth={2.5}
          dot={{ r: 5, fill: "#2563eb" }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
'''

# ---------- src/components/RatioCard.jsx ----------
FILES["src/components/RatioCard.jsx"] = '''export default function RatioCard({ label, value, suffix = "" }) {
  const display =
    typeof value === "number" ? value.toFixed(4) : value ?? "—";
  return (
    <div className="card stat">
      <div className="label">{label}</div>
      <div className="value">
        {display}
        {suffix}
      </div>
    </div>
  );
}
'''

# ---------- src/components/AnomalyList.jsx ----------
FILES["src/components/AnomalyList.jsx"] = '''export default function AnomalyList({ reasons = [], riskLevel = "Low" }) {
  return (
    <div>
      <div style={{ marginBottom: 14 }}>
        Risk Level:{" "}
        <span className={`badge ${riskLevel.toLowerCase()}`}>{riskLevel}</span>
      </div>
      {reasons.length === 0 ? (
        <p className="muted">No anomalies detected. Financial patterns look normal.</p>
      ) : (
        <ul style={{ paddingLeft: 20 }}>
          {reasons.map((reason, i) => (
            <li key={i} style={{ marginBottom: 8 }}>
              {reason}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
'''

# ---------- src/components/FeatureImportance.jsx ----------
FILES["src/components/FeatureImportance.jsx"] = '''import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export default function FeatureImportance({ data = {} }) {
  const chartData = Object.entries(data)
    .filter(([k]) => k !== "error")
    .map(([feature, importance]) => ({ feature, importance: Number(importance) }));

  if (!chartData.length) {
    return <p className="muted">No feature importance data available.</p>;
  }

  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
        <XAxis dataKey="feature" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="importance" fill="#2563eb" radius={[6, 6, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
'''

# ---------- src/pages/Login.jsx ----------
FILES["src/pages/Login.jsx"] = '''import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await login({ email, password });
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-shell">
      <div className="auth-card">
        <h1>FinSight AI</h1>
        <p className="muted">Sign in to your intelligent financial workspace</p>

        {error && <div className="error">{error}</div>}

        <form onSubmit={submit}>
          <div className="form-row">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
              autoFocus
            />
          </div>
          <div className="form-row">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" disabled={loading} style={{ width: "100%" }}>
            {loading ? "Signing in…" : "Sign In"}
          </button>
        </form>

        <p style={{ marginTop: 18, fontSize: 14, textAlign: "center" }}>
          New here? <Link to="/register">Create an account</Link>
        </p>
      </div>
    </div>
  );
}
'''

# ---------- src/pages/Register.jsx ----------
FILES["src/pages/Register.jsx"] = '''import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ full_name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const update = (key) => (e) => setForm({ ...form, [key]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await register(form);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-shell">
      <div className="auth-card">
        <h1>Create your FinSight AI account</h1>
        <p className="muted">Start analyzing financial statements in seconds</p>

        {error && <div className="error">{error}</div>}

        <form onSubmit={submit}>
          <div className="form-row">
            <label>Full Name</label>
            <input value={form.full_name} onChange={update("full_name")} required />
          </div>
          <div className="form-row">
            <label>Email</label>
            <input type="email" value={form.email} onChange={update("email")} required />
          </div>
          <div className="form-row">
            <label>Password (min 6 characters)</label>
            <input
              type="password"
              value={form.password}
              onChange={update("password")}
              required
              minLength={6}
            />
          </div>
          <button type="submit" disabled={loading} style={{ width: "100%" }}>
            {loading ? "Creating account…" : "Create Account"}
          </button>
        </form>

        <p style={{ marginTop: 18, fontSize: 14, textAlign: "center" }}>
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
'''

# ---------- src/pages/Dashboard.jsx ----------
FILES["src/pages/Dashboard.jsx"] = '''import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { createCompany, listCompanies } from "../api/client";

export default function Dashboard() {
  const [companies, setCompanies] = useState([]);
  const [form, setForm] = useState({ name: "", industry: "General", currency: "USD" });
  const [loading, setLoading] = useState(false);

  const load = async () => {
    const { data } = await listCompanies();
    setCompanies(data);
  };

  useEffect(() => {
    load();
  }, []);

  const submit = async (e) => {
    e.preventDefault();
    if (!form.name.trim()) return;
    setLoading(true);
    try {
      await createCompany(form);
      setForm({ name: "", industry: "General", currency: "USD" });
      await load();
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2 className="page-title">Your Companies</h2>

      <div className="card">
        <h3 style={{ marginTop: 0 }}>Add a Company</h3>
        <form onSubmit={submit} className="grid grid-3" style={{ alignItems: "end" }}>
          <div>
            <label>Name</label>
            <input
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              placeholder="e.g. Acme Corp"
              required
            />
          </div>
          <div>
            <label>Industry</label>
            <input
              value={form.industry}
              onChange={(e) => setForm({ ...form, industry: e.target.value })}
            />
          </div>
          <div>
            <label>Currency</label>
            <input
              value={form.currency}
              onChange={(e) => setForm({ ...form, currency: e.target.value })}
            />
          </div>
          <button type="submit" disabled={loading}>
            {loading ? "Adding…" : "+ Add Company"}
          </button>
        </form>
      </div>

      <div className="grid grid-3">
        {companies.map((c) => (
          <div key={c.id} className="card">
            <div style={{ fontWeight: 700, fontSize: 16 }}>{c.name}</div>
            <div className="muted" style={{ fontSize: 13, marginBottom: 14 }}>
              {c.industry} · {c.currency} · ID #{c.id}
            </div>
            <Link className="btn" to={`/upload?company=${c.id}`}>
              Upload Data →
            </Link>
          </div>
        ))}
        {companies.length === 0 && (
          <div
            className="card"
            style={{ gridColumn: "1 / -1", textAlign: "center", color: "#64748b" }}
          >
            No companies yet. Add one above to get started.
          </div>
        )}
      </div>
    </div>
  );
}
'''

# ---------- src/pages/Upload.jsx ----------
FILES["src/pages/Upload.jsx"] = '''import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

import { bulkUploadStatements, listCompanies, listStatements } from "../api/client";

const SAMPLE = () => {
  const rows = [];
  for (let i = 0; i < 12; i++) {
    rows.push({
      period: `2024-${String(i + 1).padStart(2, "0")}`,
      revenue: 100000 + i * 2000,
      expenses: 70000 + i * 1500,
      assets: 500000 + i * 5000,
      liabilities: 200000 + i * 1000,
      equity: 300000 + i * 4000,
      inventory: 50000,
      operating_cash_flow: 25000 + i * 500,
      investing_cash_flow: -8000,
      financing_cash_flow: 3000,
      net_profit: 20000 + i * 400,
    });
  }
  return rows;
};

export default function Upload() {
  const [params] = useSearchParams();
  const [companies, setCompanies] = useState([]);
  const [companyId, setCompanyId] = useState(params.get("company") || "");
  const [statements, setStatements] = useState([]);
  const [json, setJson] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    listCompanies().then(({ data }) => {
      setCompanies(data);
      if (!companyId && data.length) setCompanyId(String(data[0].id));
    });
  }, []);

  useEffect(() => {
    if (!companyId) return;
    listStatements(companyId).then(({ data }) => setStatements(data));
  }, [companyId]);

  const upload = async () => {
    setError("");
    setMessage("");
    try {
      const parsed = JSON.parse(json);
      if (!Array.isArray(parsed)) throw new Error("JSON must be an array of statements");
      await bulkUploadStatements(companyId, parsed);
      setMessage(`✅ Uploaded ${parsed.length} statements successfully`);
      setJson("");
      const { data } = await listStatements(companyId);
      setStatements(data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    }
  };

  const loadSample = () => {
    setJson(JSON.stringify(SAMPLE(), null, 2));
  };

  return (
    <div>
      <h2 className="page-title">Upload Financial Statements</h2>

      <div className="card">
        <div className="form-row">
          <label>Select Company</label>
          <select value={companyId} onChange={(e) => setCompanyId(e.target.value)}>
            <option value="">— choose —</option>
            {companies.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-row">
          <label>Paste JSON Array of Statements</label>
          <textarea
            rows={12}
            value={json}
            onChange={(e) => setJson(e.target.value)}
            placeholder='[{"period":"2024-01","revenue":100000,"expenses":70000,...}]'
            style={{ fontFamily: "monospace", fontSize: 13 }}
          />
        </div>

        {error && <div className="error">{error}</div>}
        {message && <div className="success">{message}</div>}

        <div style={{ display: "flex", gap: 8 }}>
          <button onClick={upload} disabled={!companyId || !json}>
            Upload
          </button>
          <button onClick={loadSample} style={{ background: "#64748b" }}>
            Load Sample Data (12 months)
          </button>
        </div>
      </div>

      <div className="card">
        <h3 style={{ marginTop: 0 }}>Existing Statements ({statements.length})</h3>
        {statements.length > 0 ? (
          <div style={{ overflowX: "auto" }}>
            <table>
              <thead>
                <tr>
                  <th>Period</th>
                  <th>Revenue</th>
                  <th>Expenses</th>
                  <th>Assets</th>
                  <th>Liabilities</th>
                  <th>Net Profit</th>
                  <th>Operating CF</th>
                </tr>
              </thead>
              <tbody>
                {statements.map((s) => (
                  <tr key={s.id}>
                    <td>{s.period}</td>
                    <td>{Number(s.revenue).toLocaleString()}</td>
                    <td>{Number(s.expenses).toLocaleString()}</td>
                    <td>{Number(s.assets).toLocaleString()}</td>
                    <td>{Number(s.liabilities).toLocaleString()}</td>
                    <td>{Number(s.net_profit).toLocaleString()}</td>
                    <td>{Number(s.operating_cash_flow).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="muted">No statements uploaded yet.</p>
        )}
      </div>
    </div>
  );
}
'''

# ---------- src/pages/Analysis.jsx ----------
FILES["src/pages/Analysis.jsx"] = '''import { useEffect, useState } from "react";

import { analyzeCompany, listCompanies } from "../api/client";
import HealthScoreGauge from "../components/HealthScoreGauge";
import RatioCard from "../components/RatioCard";

export default function Analysis() {
  const [companies, setCompanies] = useState([]);
  const [companyId, setCompanyId] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    listCompanies().then(({ data }) => {
      setCompanies(data);
      if (data.length) setCompanyId(String(data[0].id));
    });
  }, []);

  useEffect(() => {
    if (!companyId) return;
    setError("");
    setLoading(true);
    analyzeCompany(companyId)
      .then(({ data }) => setResult(data))
      .catch((err) =>
        setError(err.response?.data?.detail || "Failed to analyze")
      )
      .finally(() => setLoading(false));
  }, [companyId]);

  return (
    <div>
      <h2 className="page-title">Financial Statement Analysis</h2>

      <div className="card">
        <label>Select Company</label>
        <select value={companyId} onChange={(e) => setCompanyId(e.target.value)}>
          {companies.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      {error && <div className="error">{error}</div>}
      {loading && <p className="muted">Analyzing…</p>}

      {result && (
        <>
          <div className="card">
            <h3 style={{ marginTop: 0, textAlign: "center" }}>Financial Health Score</h3>
            <HealthScoreGauge
              score={result.score.score}
              riskLevel={result.score.risk_level}
            />
          </div>

          <div className="grid grid-4">
            <RatioCard label="Current Ratio" value={result.ratios.current_ratio} />
            <RatioCard label="Quick Ratio" value={result.ratios.quick_ratio} />
            <RatioCard label="Debt Ratio" value={result.ratios.debt_ratio} />
            <RatioCard label="ROA" value={result.ratios.roa} />
            <RatioCard label="ROE" value={result.ratios.roe} />
            <RatioCard label="Gross Margin" value={result.ratios.gross_margin} />
            <RatioCard
              label="Net Profit Margin"
              value={result.ratios.net_profit_margin}
            />
          </div>
        </>
      )}
    </div>
  );
}
'''

# ---------- src/pages/Predictions.jsx ----------
FILES["src/pages/Predictions.jsx"] = '''import { useEffect, useState } from "react";

import { listCompanies, predictCashflow } from "../api/client";
import CashFlowChart from "../components/CashFlowChart";

export default function Predictions() {
  const [companies, setCompanies] = useState([]);
  const [companyId, setCompanyId] = useState("");
  const [horizon, setHorizon] = useState(3);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    listCompanies().then(({ data }) => {
      setCompanies(data);
      if (data.length) setCompanyId(String(data[0].id));
    });
  }, []);

  const run = async () => {
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const { data } = await predictCashflow(companyId, horizon);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2 className="page-title">AI Cash Flow Prediction</h2>

      <div className="card">
        <div className="grid grid-3" style={{ alignItems: "end" }}>
          <div>
            <label>Company</label>
            <select value={companyId} onChange={(e) => setCompanyId(e.target.value)}>
              {companies.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label>Horizon (future periods)</label>
            <input
              type="number"
              min="1"
              max="12"
              value={horizon}
              onChange={(e) => setHorizon(Number(e.target.value))}
            />
          </div>
          <button onClick={run} disabled={loading || !companyId}>
            {loading ? "Predicting…" : "🔮 Predict"}
          </button>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      {result && (
        <>
          <div className="card">
            <div className="grid grid-3">
              <div className="stat">
                <div className="label">Model</div>
                <div className="value" style={{ fontSize: 18 }}>
                  {result.model_name}
                </div>
              </div>
              <div className="stat">
                <div className="label">Confidence</div>
                <div className="value">
                  {(result.confidence * 100).toFixed(0)}%
                </div>
              </div>
              <div className="stat">
                <div className="label">Next Period</div>
                <div className="value">
                  {result.predicted_values[0]?.toLocaleString()}
                </div>
              </div>
            </div>
          </div>

          <div className="card">
            <h3 style={{ marginTop: 0 }}>Projected Cash Flow</h3>
            <CashFlowChart values={result.predicted_values} />
          </div>
        </>
      )}
    </div>
  );
}
'''

# ---------- src/pages/Anomalies.jsx ----------
FILES["src/pages/Anomalies.jsx"] = '''import { useEffect, useState } from "react";

import { detectAnomalies, listCompanies } from "../api/client";
import AnomalyList from "../components/AnomalyList";

export default function Anomalies() {
  const [companies, setCompanies] = useState([]);
  const [companyId, setCompanyId] = useState("");
  const [result, setResult] = useState(null);

  useEffect(() => {
    listCompanies().then(({ data }) => {
      setCompanies(data);
      if (data.length) setCompanyId(String(data[0].id));
    });
  }, []);

  useEffect(() => {
    if (!companyId) return;
    detectAnomalies(companyId).then(({ data }) => setResult(data));
  }, [companyId]);

  return (
    <div>
      <h2 className="page-title">Financial Anomaly Detection</h2>

      <div className="card">
        <label>Select Company</label>
        <select value={companyId} onChange={(e) => setCompanyId(e.target.value)}>
          {companies.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      {result && (
        <div className="card">
          <h3 style={{ marginTop: 0 }}>Results</h3>
          <p className="muted">
            {result.indices.length} anomalous period(s) flagged out of the uploaded data.
          </p>
          <AnomalyList reasons={result.reasons} riskLevel={result.risk_level} />
        </div>
      )}
    </div>
  );
}
'''

# ---------- src/pages/Reports.jsx ----------
FILES["src/pages/Reports.jsx"] = '''import { useEffect, useState } from "react";

import {
  downloadReportPdf,
  getReport,
  listCompanies,
} from "../api/client";
import HealthScoreGauge from "../components/HealthScoreGauge";

export default function Reports() {
  const [companies, setCompanies] = useState([]);
  const [companyId, setCompanyId] = useState("");
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    listCompanies().then(({ data }) => {
      setCompanies(data);
      if (data.length) setCompanyId(String(data[0].id));
    });
  }, []);

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      const { data } = await getReport(companyId);
      setReport(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to generate report");
    } finally {
      setLoading(false);
    }
  };

  const downloadPdf = async () => {
    try {
      const { data } = await downloadReportPdf(companyId);
      const url = URL.createObjectURL(new Blob([data], { type: "application/pdf" }));
      const a = document.createElement("a");
      a.href = url;
      a.download = `finsight_report_${companyId}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError("PDF download failed");
    }
  };

  return (
    <div>
      <h2 className="page-title">Financial Reports</h2>

      <div className="card">
        <div className="grid grid-3" style={{ alignItems: "end" }}>
          <div>
            <label>Select Company</label>
            <select value={companyId} onChange={(e) => setCompanyId(e.target.value)}>
              {companies.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>
          <button onClick={load} disabled={loading || !companyId}>
            {loading ? "Generating…" : "Generate Report"}
          </button>
          {report && (
            <button onClick={downloadPdf} className="btn-success">
              ⬇ Download PDF
            </button>
          )}
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      {report && (
        <>
          <div className="card">
            <h3 style={{ marginTop: 0, textAlign: "center" }}>Health Score</h3>
            <HealthScoreGauge
              score={report.score.score}
              riskLevel={report.score.risk_level}
            />
          </div>

          <div className="card">
            <h3 style={{ marginTop: 0 }}>💡 Recommendations</h3>
            {report.recommendations.map((rec, i) => (
              <div key={i} className="recommendation">
                {rec}
              </div>
            ))}
          </div>

          <div className="card">
            <h3 style={{ marginTop: 0 }}>Cash Flow Forecast</h3>
            <ul>
              {report.predictions.predicted_values.map((v, i) => (
                <li key={i}>
                  Period +{i + 1}: <strong>{Number(v).toLocaleString()}</strong>
                </li>
              ))}
            </ul>
          </div>
        </>
      )}
    </div>
  );
}
'''

# ---------- src/App.jsx ----------
FILES["src/App.jsx"] = '''import { Navigate, Route, Routes } from "react-router-dom";

import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import Analysis from "./pages/Analysis";
import Anomalies from "./pages/Anomalies";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Predictions from "./pages/Predictions";
import Register from "./pages/Register";
import Reports from "./pages/Reports";
import Upload from "./pages/Upload";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="upload" element={<Upload />} />
        <Route path="analysis" element={<Analysis />} />
        <Route path="predictions" element={<Predictions />} />
        <Route path="anomalies" element={<Anomalies />} />
        <Route path="reports" element={<Reports />} />
      </Route>

      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
'''

# ---------- Write all files ----------
def main():
    count = 0
    for rel_path, content in FILES.items():
        p = ROOT / rel_path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content.lstrip("\\n"), encoding="utf-8")
        count += 1
        print(f"  created  {rel_path}")
    print(f"\\nDone. {count} frontend files written to {ROOT}")


if __name__ == "__main__":
    main()