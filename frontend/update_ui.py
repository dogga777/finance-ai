"""FinSight AI - UI/UX graphics upgrade."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "src"
FILES = {}

# =====================================================
# components/Icons.jsx  — inline SVG icon library
# =====================================================
FILES["components/Icons.jsx"] = '''
export const IconDashboard = ({ size = 18 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="3" width="7" height="9" rx="1.5" />
    <rect x="14" y="3" width="7" height="5" rx="1.5" />
    <rect x="14" y="12" width="7" height="9" rx="1.5" />
    <rect x="3" y="16" width="7" height="5" rx="1.5" />
  </svg>
);

export const IconUpload = ({ size = 18 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
    <polyline points="17 8 12 3 7 8" />
    <line x1="12" y1="3" x2="12" y2="15" />
  </svg>
);

export const IconChart = ({ size = 18 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="18" y1="20" x2="18" y2="10" />
    <line x1="12" y1="20" x2="12" y2="4" />
    <line x1="6" y1="20" x2="6" y2="14" />
  </svg>
);

export const IconTrending = ({ size = 18 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
    <polyline points="17 6 23 6 23 12" />
  </svg>
);

export const IconAlert = ({ size = 18 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
    <line x1="12" y1="9" x2="12" y2="13" />
    <line x1="12" y1="17" x2="12.01" y2="17" />
  </svg>
);

export const IconFile = ({ size = 18 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
    <polyline points="14 2 14 8 20 8" />
    <line x1="16" y1="13" x2="8" y2="13" />
    <line x1="16" y1="17" x2="8" y2="17" />
  </svg>
);

export const IconBuilding = ({ size = 24 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <rect x="4" y="2" width="16" height="20" rx="2" />
    <line x1="9" y1="6" x2="9" y2="6.01" />
    <line x1="15" y1="6" x2="15" y2="6.01" />
    <line x1="9" y1="10" x2="9" y2="10.01" />
    <line x1="15" y1="10" x2="15" y2="10.01" />
    <line x1="9" y1="14" x2="9" y2="14.01" />
    <line x1="15" y1="14" x2="15" y2="14.01" />
    <path d="M9 22v-4h6v4" />
  </svg>
);

export const IconSparkles = ({ size = 20 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1" />
    <circle cx="12" cy="12" r="3" />
  </svg>
);

export const IconShield = ({ size = 20 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    <polyline points="9 12 11 14 15 10" />
  </svg>
);

export const IconBolt = ({ size = 20 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
  </svg>
);

export const IconDownload = ({ size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
    <polyline points="7 10 12 15 17 10" />
    <line x1="12" y1="15" x2="12" y2="3" />
  </svg>
);

export const IconPlus = ({ size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
    <line x1="12" y1="5" x2="12" y2="19" />
    <line x1="5" y1="12" x2="19" y2="12" />
  </svg>
);

export const IconRefresh = ({ size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="23 4 23 10 17 10" />
    <polyline points="1 20 1 14 7 14" />
    <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
  </svg>
);

export const IconEmpty = ({ size = 80 }) => (
  <svg width={size} height={size} viewBox="0 0 120 120" fill="none">
    <circle cx="60" cy="60" r="50" fill="url(#g1)" opacity="0.15" />
    <circle cx="60" cy="60" r="35" fill="url(#g1)" opacity="0.1" />
    <rect x="35" y="40" width="50" height="42" rx="6" fill="#fff" stroke="#cbd5e1" strokeWidth="2" />
    <line x1="44" y1="52" x2="76" y2="52" stroke="#cbd5e1" strokeWidth="2" strokeLinecap="round" />
    <line x1="44" y1="60" x2="68" y2="60" stroke="#e2e8f0" strokeWidth="2" strokeLinecap="round" />
    <line x1="44" y1="68" x2="72" y2="68" stroke="#e2e8f0" strokeWidth="2" strokeLinecap="round" />
    <defs>
      <linearGradient id="g1" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stopColor="#4f6ef7" />
        <stop offset="100%" stopColor="#8b5cf6" />
      </linearGradient>
    </defs>
  </svg>
);
'''

# =====================================================
# components/Layout.jsx — proper SVG nav icons
# =====================================================
FILES["components/Layout.jsx"] = '''
import { NavLink, Outlet, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";
import {
  IconDashboard,
  IconUpload,
  IconChart,
  IconTrending,
  IconAlert,
  IconFile,
} from "./Icons";

const links = [
  { to: "/dashboard", label: "Dashboard", Icon: IconDashboard },
  { to: "/upload", label: "Upload Data", Icon: IconUpload },
  { to: "/analysis", label: "Analysis", Icon: IconChart },
  { to: "/predictions", label: "Predictions", Icon: IconTrending },
  { to: "/anomalies", label: "Anomalies", Icon: IconAlert },
  { to: "/reports", label: "Reports", Icon: IconFile },
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

        <div className="nav-section-label">Workspace</div>

        <nav className="nav-list">
          {links.map(({ to, label, Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) => (isActive ? "active" : "")}
            >
              <span className="nav-icon"><Icon size={18} /></span>
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="user-chip">
            <div className="user-avatar">
              {user?.full_name?.[0]?.toUpperCase() || "U"}
            </div>
            <div className="user-meta">
              <div className="user-name">{user?.full_name || "User"}</div>
              <div className="user-email">{user?.email}</div>
            </div>
          </div>
          <button className="btn-ghost" onClick={handleLogout}>
            Sign out
          </button>
        </div>
      </aside>

      <div className="main">
        <header className="topbar">
          <div className="title">Intelligent Financial Analytics</div>
          <div className="actions">
            <div className="status-pill">
              <span className="status-dot" />
              API Online
            </div>
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

# =====================================================
# pages/Dashboard.jsx — hero + stat cards + rich company cards
# =====================================================
FILES["pages/Dashboard.jsx"] = '''
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { createCompany, listCompanies } from "../api/client";
import {
  IconBuilding,
  IconPlus,
  IconSparkles,
  IconTrending,
  IconShield,
} from "../components/Icons";

export default function Dashboard() {
  const { user } = (() => ({}))(); // placeholder to keep hooks order
  const [companies, setCompanies] = useState([]);
  const [form, setForm] = useState({ name: "", industry: "General", currency: "USD" });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

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
    setMessage("");
    try {
      await createCompany(form);
      setForm({ name: "", industry: "General", currency: "USD" });
      setMessage("Company added successfully");
      await load();
    } catch (err) {
      setMessage(err.response?.data?.detail || "Failed to add company");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* ---------- Hero ---------- */}
      <div className="hero">
        <div className="hero-content">
          <div className="hero-badge">
            <IconSparkles size={14} />
            AI-Powered Financial Intelligence
          </div>
          <h1 className="hero-title">Your Companies</h1>
          <p className="hero-subtitle">
            Analyze financial statements, forecast cash flow, and detect anomalies —
            all in one intelligent workspace.
          </p>
        </div>
        <div className="hero-decor" />
      </div>

      {/* ---------- Stat strip ---------- */}
      <div className="stats-strip">
        <div className="stat-tile">
          <div className="stat-tile-icon" style={{ background: "linear-gradient(135deg,#4f6ef7,#6366f1)" }}>
            <IconBuilding size={20} />
          </div>
          <div>
            <div className="stat-tile-label">Companies</div>
            <div className="stat-tile-value">{companies.length}</div>
          </div>
        </div>
        <div className="stat-tile">
          <div className="stat-tile-icon" style={{ background: "linear-gradient(135deg,#8b5cf6,#ec4899)" }}>
            <IconTrending size={20} />
          </div>
          <div>
            <div className="stat-tile-label">Forecasting Models</div>
            <div className="stat-tile-value">Ready</div>
          </div>
        </div>
        <div className="stat-tile">
          <div className="stat-tile-icon" style={{ background: "linear-gradient(135deg,#10b981,#059669)" }}>
            <IconShield size={20} />
          </div>
          <div>
            <div className="stat-tile-label">Explainable AI</div>
            <div className="stat-tile-value">Active</div>
          </div>
        </div>
      </div>

      {/* ---------- Add Company ---------- */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">Add a Company</h3>
            <p className="card-subtitle">Set up a new workspace for financial analysis</p>
          </div>
        </div>
        <form onSubmit={submit} className="grid grid-3" style={{ alignItems: "end" }}>
          <div>
            <label>Company Name</label>
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
            <IconPlus size={16} />
            {loading ? "Adding…" : "Add Company"}
          </button>
        </form>
        {message && <div className="success" style={{ marginTop: 14 }}>{message}</div>}
      </div>

      {/* ---------- Company Grid ---------- */}
      <div className="section-heading">
        <h3>Your Workspaces</h3>
        <span className="muted" style={{ fontSize: 13 }}>
          {companies.length} {companies.length === 1 ? "company" : "companies"}
        </span>
      </div>

      {companies.length === 0 ? (
        <div className="card empty-state">
          <IconBuilding size={64} />
          <h3>No companies yet</h3>
          <p className="muted">Add your first company above to start analyzing financial data.</p>
        </div>
      ) : (
        <div className="grid grid-3">
          {companies.map((c) => (
            <div key={c.id} className="company-card">
              <div className="company-card-top">
                <div className="company-avatar">
                  {c.name.slice(0, 2).toUpperCase()}
                </div>
                <div className="company-id">ID #{c.id}</div>
              </div>
              <h3 className="company-name">{c.name}</h3>
              <div className="company-meta">
                <span className="chip">{c.industry}</span>
                <span className="chip">{c.currency}</span>
              </div>
              <div className="company-actions">
                <Link className="btn" to={`/upload?company=${c.id}`}>
                  Upload Data
                </Link>
                <Link className="btn btn-ghost-dark" to="/analysis">
                  Analyze
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
'''

# =====================================================
# pages/Analysis.jsx — richer visual layout
# =====================================================
FILES["pages/Analysis.jsx"] = '''
import { useEffect, useState } from "react";

import { analyzeCompany, listCompanies } from "../api/client";
import HealthScoreGauge from "../components/HealthScoreGauge";
import RatioCard from "../components/RatioCard";
import { IconChart, IconEmpty } from "../components/Icons";

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
    setResult(null);
    analyzeCompany(companyId)
      .then(({ data }) => setResult(data))
      .catch((err) =>
        setError(err.response?.data?.detail || "Failed to analyze")
      )
      .finally(() => setLoading(false));
  }, [companyId]);

  return (
    <div>
      <div className="page-header">
        <div className="page-icon" style={{ background: "linear-gradient(135deg,#4f6ef7,#6366f1)" }}>
          <IconChart size={22} />
        </div>
        <div>
          <h2 className="page-title">Financial Statement Analysis</h2>
          <p className="page-subtitle">Automated ratio analysis and AI-generated health score</p>
        </div>
      </div>

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
      {loading && (
        <div className="card skeleton-card">
          <div className="skeleton" style={{ height: 40, width: "40%" }} />
          <div className="skeleton" style={{ height: 160, marginTop: 16 }} />
        </div>
      )}

      {result && (
        <>
          <div className="card score-card">
            <div className="score-card-left">
              <div className="score-card-label">Financial Health Score</div>
              <p className="muted" style={{ margin: "4px 0 0" }}>
                Computed from 7 financial ratios using weighted scoring
              </p>
            </div>
            <div className="score-card-right">
              <HealthScoreGauge
                score={result.score.score}
                riskLevel={result.score.risk_level}
              />
            </div>
          </div>

          <div className="section-heading">
            <h3>Financial Ratios</h3>
            <span className="muted" style={{ fontSize: 13 }}>
              Latest period
            </span>
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

# =====================================================
# pages/Predictions.jsx — richer hero + stat row
# =====================================================
FILES["pages/Predictions.jsx"] = '''
import { useEffect, useState } from "react";

import { listCompanies, predictCashflow } from "../api/client";
import CashFlowChart from "../components/CashFlowChart";
import { IconTrending, IconBolt } from "../components/Icons";

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

  const total = result?.predicted_values?.reduce((a, b) => a + b, 0) || 0;
  const avg = result?.predicted_values?.length
    ? total / result.predicted_values.length
    : 0;

  return (
    <div>
      <div className="page-header">
        <div className="page-icon" style={{ background: "linear-gradient(135deg,#8b5cf6,#ec4899)" }}>
          <IconTrending size={22} />
        </div>
        <div>
          <h2 className="page-title">AI Cash Flow Prediction</h2>
          <p className="page-subtitle">
            Random Forest forecasting based on historical financial trends
          </p>
        </div>
      </div>

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
            <label>Forecast Horizon (periods)</label>
            <input
              type="number"
              min="1"
              max="12"
              value={horizon}
              onChange={(e) => setHorizon(Number(e.target.value))}
            />
          </div>
          <button onClick={run} disabled={loading || !companyId}>
            <IconBolt size={16} />
            {loading ? "Forecasting…" : "Run Prediction"}
          </button>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      {loading && (
        <div className="card">
          <div className="skeleton" style={{ height: 300 }} />
        </div>
      )}

      {result && (
        <>
          <div className="stats-strip">
            <div className="stat-tile">
              <div className="stat-tile-icon" style={{ background: "linear-gradient(135deg,#4f6ef7,#6366f1)" }}>
                <IconBolt size={20} />
              </div>
              <div>
                <div className="stat-tile-label">Model</div>
                <div className="stat-tile-value" style={{ fontSize: 16 }}>
                  {result.model_name}
                </div>
              </div>
            </div>
            <div className="stat-tile">
              <div className="stat-tile-icon" style={{ background: "linear-gradient(135deg,#10b981,#059669)" }}>
                <IconTrending size={20} />
              </div>
              <div>
                <div className="stat-tile-label">Confidence</div>
                <div className="stat-tile-value">
                  {(result.confidence * 100).toFixed(0)}%
                </div>
              </div>
            </div>
            <div className="stat-tile">
              <div className="stat-tile-icon" style={{ background: "linear-gradient(135deg,#f59e0b,#ef4444)" }}>
                <IconTrending size={20} />
              </div>
              <div>
                <div className="stat-tile-label">Avg / Period</div>
                <div className="stat-tile-value" style={{ fontSize: 18 }}>
                  {avg.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                </div>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="card-header">
              <div>
                <h3 className="card-title">Projected Cash Flow</h3>
                <p className="card-subtitle">Forecast for the next {horizon} periods</p>
              </div>
            </div>
            <CashFlowChart values={result.predicted_values} />
          </div>

          <div className="card">
            <h3 className="card-title">Forecast Details</h3>
            <table style={{ marginTop: 12 }}>
              <thead>
                <tr>
                  <th>Period</th>
                  <th>Predicted Cash Flow</th>
                  <th>Change vs Previous</th>
                </tr>
              </thead>
              <tbody>
                {result.predicted_values.map((v, i) => {
                  const prev = i === 0 ? null : result.predicted_values[i - 1];
                  const delta = prev ? ((v - prev) / Math.abs(prev)) * 100 : null;
                  return (
                    <tr key={i}>
                      <td>Period +{i + 1}</td>
                      <td><strong>{Number(v).toLocaleString()}</strong></td>
                      <td>
                        {delta === null ? (
                          <span className="muted">—</span>
                        ) : (
                          <span style={{ color: delta >= 0 ? "#10b981" : "#ef4444", fontWeight: 600 }}>
                            {delta >= 0 ? "▲" : "▼"} {Math.abs(delta).toFixed(2)}%
                          </span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}
'''

# =====================================================
# pages/Reports.jsx — rich report layout
# =====================================================
FILES["pages/Reports.jsx"] = '''
import { useEffect, useState } from "react";

import { downloadReportPdf, getReport, listCompanies } from "../api/client";
import HealthScoreGauge from "../components/HealthScoreGauge";
import {
  IconFile,
  IconDownload,
  IconSparkles,
  IconTrending,
} from "../components/Icons";

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
    } catch {
      setError("PDF download failed");
    }
  };

  return (
    <div>
      <div className="page-header">
        <div className="page-icon" style={{ background: "linear-gradient(135deg,#10b981,#059669)" }}>
          <IconFile size={22} />
        </div>
        <div>
          <h2 className="page-title">Financial Reports</h2>
          <p className="page-subtitle">
            Comprehensive analysis with health score, forecast, and AI recommendations
          </p>
        </div>
      </div>

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
              <IconDownload size={16} />
              Download PDF
            </button>
          )}
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      {report && (
        <>
          <div className="score-card">
            <div className="score-card-left">
              <div className="score-card-label">Overall Financial Health</div>
              <p className="muted" style={{ margin: "4px 0 0" }}>
                Based on automated ratio analysis and ML-driven risk evaluation
              </p>
              <div style={{ marginTop: 16 }}>
                <span className={`badge ${report.score.risk_level.toLowerCase()}`}>
                  {report.score.risk_level} Risk
                </span>
              </div>
            </div>
            <div className="score-card-right">
              <HealthScoreGauge
                score={report.score.score}
                riskLevel={report.score.risk_level}
              />
            </div>
          </div>

          <div className="card">
            <div className="card-header">
              <div className="header-icon-wrap" style={{ background: "linear-gradient(135deg,#f59e0b,#ef4444)" }}>
                <IconSparkles size={18} />
              </div>
              <div>
                <h3 className="card-title">AI Recommendations</h3>
                <p className="card-subtitle">Strategic actions based on your data</p>
              </div>
            </div>
            <div style={{ marginTop: 16 }}>
              {report.recommendations.map((rec, i) => (
                <div key={i} className="recommendation">
                  <span className="rec-num">{i + 1}</span>
                  {rec}
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <div className="card-header">
              <div className="header-icon-wrap" style={{ background: "linear-gradient(135deg,#8b5cf6,#ec4899)" }}>
                <IconTrending size={18} />
              </div>
              <div>
                <h3 className="card-title">Cash Flow Forecast</h3>
                <p className="card-subtitle">Projected next 3 periods</p>
              </div>
            </div>
            <table style={{ marginTop: 12 }}>
              <thead>
                <tr>
                  <th>Period</th>
                  <th>Predicted Cash Flow</th>
                </tr>
              </thead>
              <tbody>
                {report.predictions.predicted_values.map((v, i) => (
                  <tr key={i}>
                    <td>Period +{i + 1}</td>
                    <td><strong>{Number(v).toLocaleString()}</strong></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}
'''

# =====================================================
# components/RatioCard.jsx — richer visual
# =====================================================
FILES["components/RatioCard.jsx"] = '''
export default function RatioCard({ label, value, suffix = "" }) {
  const display = typeof value === "number" ? value.toFixed(4) : value ?? "—";

  // Determine a color based on value category
  let trend = "neutral";
  if (typeof value === "number") {
    if (label.toLowerCase().includes("debt")) {
      trend = value < 0.5 ? "good" : value < 0.7 ? "warn" : "bad";
    } else {
      trend = value > 0 ? "good" : "bad";
    }
  }

  return (
    <div className="ratio-card">
      <div className="ratio-label">{label}</div>
      <div className={`ratio-value ratio-${trend}`}>
        {display}
        {suffix}
      </div>
      <div className="ratio-bar">
        <div className={`ratio-bar-fill ratio-fill-${trend}`} />
      </div>
    </div>
  );
}
'''

# =====================================================
# components/HealthScoreGauge.jsx — prettier gauge
# =====================================================
FILES["components/HealthScoreGauge.jsx"] = '''
export default function HealthScoreGauge({ score = 0, riskLevel = "Unknown" }) {
  const radius = 80;
  const circumference = Math.PI * radius;
  const progress = (Math.max(0, Math.min(100, score)) / 100) * circumference;

  const color =
    riskLevel === "Low" ? "#10b981" : riskLevel === "Medium" ? "#f59e0b" : "#ef4444";
  const gradId = "gauge-" + riskLevel.toLowerCase();

  return (
    <div style={{ textAlign: "center", padding: "6px 0" }}>
      <svg viewBox="0 0 200 120" width="280" height="170">
        <defs>
          <linearGradient id={gradId} x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor={color} stopOpacity="0.7" />
            <stop offset="100%" stopColor={color} />
          </linearGradient>
        </defs>
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke="#f1f5f9"
          strokeWidth="16"
          strokeLinecap="round"
        />
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke={`url(#${gradId})`}
          strokeWidth="16"
          strokeLinecap="round"
          strokeDasharray={`${progress} ${circumference}`}
          style={{ transition: "stroke-dasharray 800ms cubic-bezier(0.4,0,0.2,1)" }}
        />
        <text x="100" y="88" textAnchor="middle" fontSize="34" fontWeight="800" fill="#0f172a" letterSpacing="-1">
          {score}
        </text>
        <text x="100" y="108" textAnchor="middle" fontSize="12" fill="#94a3b8" fontWeight="500">
          OUT OF 100
        </text>
      </svg>
      <div style={{ marginTop: 4 }}>
        <span className={`badge ${riskLevel.toLowerCase()}`}>{riskLevel} Risk</span>
      </div>
    </div>
  );
}
'''

# =====================================================
# index.css — additional graphic styles
# =====================================================
FILES["index.css"] = '''
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --bg-page: #f6f7f9;
  --bg-surface: #ffffff;
  --bg-sidebar: #0b1120;
  --bg-sidebar-hover: #151f34;

  --accent: #4f6ef7;
  --accent-hover: #3a5beb;
  --accent-soft: #eef1fe;

  --success: #10b981;
  --success-soft: #d1fae5;
  --warning: #f59e0b;
  --warning-soft: #fef3c7;
  --danger: #ef4444;
  --danger-soft: #fee2e2;

  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-muted: #94a3b8;
  --text-sidebar: #94a3b8;

  --border: #e5e7eb;
  --border-soft: #f1f5f9;

  --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.06), 0 1px 2px rgba(15, 23, 42, 0.04);
  --shadow-md: 0 4px 12px rgba(15, 23, 42, 0.06);
  --shadow-glow: 0 8px 24px rgba(79, 110, 247, 0.35);

  --radius: 12px;
  --radius-lg: 16px;
  --radius-xl: 20px;
  --transition: 160ms cubic-bezier(0.4, 0, 0.2, 1);
}

* { box-sizing: border-box; -webkit-font-smoothing: antialiased; }
html, body, #root { height: 100%; }
body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 14px;
  color: var(--text-primary);
  background: var(--bg-page);
  line-height: 1.5;
}

a { color: var(--accent); text-decoration: none; transition: color var(--transition); }
a:hover { color: var(--accent-hover); }

/* ============ App shell ============ */
.app-shell { display: flex; min-height: 100vh; }

.sidebar {
  width: 268px;
  flex-shrink: 0;
  background: var(--bg-sidebar);
  background-image:
    radial-gradient(ellipse 200% 60% at 50% 0%, rgba(79, 110, 247, 0.18), transparent),
    linear-gradient(180deg, #0b1120 0%, #070c17 100%);
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  position: relative;
}

.sidebar .brand {
  color: #fff;
  font-size: 19px;
  font-weight: 800;
  letter-spacing: -0.5px;
  margin-bottom: 24px;
  padding: 0 12px 0 0;
  display: flex;
  align-items: center;
  gap: 10px;
}
.sidebar .brand::before {
  content: '';
  width: 32px;
  height: 32px;
  border-radius: 9px;
  background: linear-gradient(135deg, #4f6ef7, #8b5cf6);
  box-shadow: 0 6px 18px rgba(79, 110, 247, 0.5);
  flex-shrink: 0;
}
.sidebar .brand span {
  background: linear-gradient(135deg, #93b4ff, #c4b5fd);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-section-label {
  color: #475569;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  padding: 0 12px;
  margin-bottom: 8px;
}

.nav-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.sidebar a {
  color: var(--text-sidebar);
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all var(--transition);
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
}

.sidebar a .nav-icon {
  display: inline-flex;
  opacity: 0.85;
}

.sidebar a:hover {
  background: var(--bg-sidebar-hover);
  color: #fff;
}
.sidebar a.active {
  background: linear-gradient(135deg, rgba(79, 110, 247, 0.95), rgba(139, 92, 246, 0.85));
  color: #fff;
  box-shadow: 0 4px 16px rgba(79, 110, 247, 0.4), inset 0 1px 0 rgba(255,255,255,0.18);
}
.sidebar a.active .nav-icon { opacity: 1; }

.sidebar-footer {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #1e293b;
}

.user-chip {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  border-radius: 10px;
  background: rgba(255,255,255,0.03);
  margin-bottom: 10px;
}
.user-avatar {
  width: 34px;
  height: 34px;
  border-radius: 9px;
  background: linear-gradient(135deg, #4f6ef7, #8b5cf6);
  color: #fff;
  font-weight: 700;
  font-size: 14px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
}
.user-meta { min-width: 0; flex: 1; }
.user-name {
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.user-email {
  color: #64748b;
  font-size: 11px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.btn-ghost {
  width: 100%;
  background: rgba(255,255,255,0.05);
  color: #cbd5e1;
  box-shadow: none;
  font-size: 13px;
  padding: 9px 12px;
}
.btn-ghost:hover:not(:disabled) {
  background: rgba(255,255,255,0.1);
  color: #fff;
  transform: none;
  box-shadow: none;
}

/* ============ Main ============ */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  background: var(--bg-page);
}

.topbar {
  height: 68px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: saturate(180%) blur(12px);
  -webkit-backdrop-filter: saturate(180%) blur(12px);
  border-bottom: 1px solid var(--border-soft);
  position: sticky;
  top: 0;
  z-index: 10;
}
.topbar .title {
  font-weight: 600;
  font-size: 15px;
  color: var(--text-secondary);
}
.topbar .actions { display: flex; gap: 12px; align-items: center; }

.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: var(--success-soft);
  color: #065f46;
  font-size: 12px;
  font-weight: 600;
  border-radius: 999px;
}
.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--success);
  box-shadow: 0 0 0 3px rgba(16,185,129,0.2);
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 3px rgba(16,185,129,0.2); }
  50% { box-shadow: 0 0 0 6px rgba(16,185,129,0.1); }
}

.content {
  padding: 32px;
  max-width: 1280px;
  width: 100%;
  margin: 0 auto;
  animation: fadeInUp 320ms cubic-bezier(0.4, 0, 0.2, 1);
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ============ Hero ============ */
.hero {
  position: relative;
  padding: 32px;
  border-radius: var(--radius-xl);
  background:
    radial-gradient(circle at 90% 20%, rgba(139, 92, 246, 0.4), transparent 50%),
    linear-gradient(135deg, #0b1120 0%, #1e1b4b 100%);
  margin-bottom: 24px;
  overflow: hidden;
  color: #fff;
}
.hero-content { position: relative; z-index: 2; max-width: 640px; }
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  border-radius: 999px;
  background: rgba(79, 110, 247, 0.2);
  border: 1px solid rgba(79, 110, 247, 0.35);
  color: #c7d2fe;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 14px;
}
.hero-title {
  font-size: 32px;
  font-weight: 800;
  letter-spacing: -1px;
  margin: 0 0 8px;
  background: linear-gradient(135deg, #fff 0%, #c7d2fe 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-subtitle {
  color: #94a3b8;
  font-size: 15px;
  margin: 0;
  line-height: 1.6;
}
.hero-decor {
  position: absolute;
  inset: 0;
  background-image:
    radial-gradient(circle at 15% 80%, rgba(79, 110, 247, 0.5), transparent 40%),
    radial-gradient(circle at 85% 30%, rgba(236, 72, 153, 0.25), transparent 40%);
  z-index: 1;
  pointer-events: none;
}

/* ============ Stats strip ============ */
.stats-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}
.stat-tile {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition);
}
.stat-tile:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}
.stat-tile-icon {
  width: 44px;
  height: 44px;
  border-radius: 11px;
  color: #fff;
  display: grid;
  place-items: center;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
  flex-shrink: 0;
}
.stat-tile-label {
  color: var(--text-muted);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  font-weight: 600;
  margin-bottom: 2px;
}
.stat-tile-value {
  font-size: 22px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.5px;
}

/* ============ Page header ============ */
.page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}
.page-icon {
  width: 52px;
  height: 52px;
  border-radius: 13px;
  color: #fff;
  display: grid;
  place-items: center;
  box-shadow: 0 6px 20px rgba(15, 23, 42, 0.18);
  flex-shrink: 0;
}
.page-title {
  margin: 0;
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.7px;
}
.page-subtitle {
  margin: 2px 0 0;
  color: var(--text-muted);
  font-size: 14px;
}

/* ============ Cards ============ */
.card {
  background: var(--bg-surface);
  border-radius: var(--radius-lg);
  padding: 24px;
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  margin-bottom: 20px;
  transition: box-shadow var(--transition);
}
.card:hover { box-shadow: var(--shadow-md); }

.card-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 8px;
}
.header-icon-wrap {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  color: #fff;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
}
.card-title {
  margin: 0;
  font-size: 17px;
  font-weight: 700;
  letter-spacing: -0.3px;
}
.card-subtitle {
  margin: 2px 0 0;
  color: var(--text-muted);
  font-size: 13px;
}

.section-heading {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin: 24px 0 12px;
}
.section-heading h3 {
  margin: 0;
  font-size: 17px;
  font-weight: 700;
  letter-spacing: -0.3px;
}

/* ============ Grids ============ */
.grid { display: grid; gap: 16px; }
.grid-2 { grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }
.grid-3 { grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }
.grid-4 { grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }

/* ============ Buttons ============ */
button, .btn {
  background: linear-gradient(135deg, var(--accent), #6366f1);
  color: #fff;
  border: none;
  padding: 11px 18px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  letter-spacing: -0.1px;
  transition: all var(--transition);
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.08), 0 1px 3px rgba(79, 110, 247, 0.15);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  text-decoration: none;
}
button:hover:not(:disabled), .btn:hover {
  background: linear-gradient(135deg, var(--accent-hover), #4f46e5);
  box-shadow: var(--shadow-glow);
  transform: translateY(-1px);
  color: #fff;
}
button:active:not(:disabled), .btn:active { transform: translateY(0); }
button:disabled { opacity: 0.5; cursor: not-allowed; box-shadow: none; }

.btn-success {
  background: linear-gradient(135deg, #10b981, #059669);
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.08), 0 1px 3px rgba(16, 185, 129, 0.2);
}
.btn-success:hover:not(:disabled) {
  background: linear-gradient(135deg, #059669, #047857);
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4);
}
.btn-ghost-dark {
  background: #f1f5f9;
  color: #334155;
  box-shadow: none;
}
.btn-ghost-dark:hover:not(:disabled) {
  background: #e2e8f0;
  color: #0f172a;
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

/* ============ Inputs ============ */
input, textarea, select {
  width: 100%;
  padding: 11px 14px;
  border: 1px solid var(--border);
  border-radius: 10px;
  font-size: 14px;
  font-family: inherit;
  background: #fff;
  color: var(--text-primary);
  transition: all var(--transition);
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
}
input:hover, textarea:hover, select:hover { border-color: #cbd5e1; }
input:focus, textarea:focus, select:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 4px var(--accent-soft);
}
input::placeholder, textarea::placeholder { color: var(--text-muted); }

label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
  letter-spacing: -0.1px;
}
.form-row { margin-bottom: 16px; }
textarea { resize: vertical; line-height: 1.6; }

/* ============ Tables ============ */
table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 14px;
}
th, td {
  padding: 12px 14px;
  text-align: left;
  border-bottom: 1px solid var(--border-soft);
}
th {
  color: var(--text-muted);
  font-weight: 600;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  background: #fafbfc;
}
tbody tr { transition: background var(--transition); }
tbody tr:hover { background: #f8fafc; }
tbody tr:last-child td { border-bottom: none; }

/* ============ Badges / chips ============ */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: -0.1px;
  line-height: 1.4;
}
.badge::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  flex-shrink: 0;
}
.badge.low { background: var(--success-soft); color: #047857; }
.badge.medium { background: var(--warning-soft); color: #b45309; }
.badge.high { background: var(--danger-soft); color: #b91c1c; }

.chip {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 6px;
  background: #f1f5f9;
  color: #475569;
  font-size: 12px;
  font-weight: 600;
}

/* ============ Company cards ============ */
.company-card {
  position: relative;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px;
  box-shadow: var(--shadow-sm);
  transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.company-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.10);
  border-color: #c7d2fe;
}
.company-card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.company-avatar {
  width: 44px;
  height: 44px;
  border-radius: 11px;
  background: linear-gradient(135deg, #4f6ef7, #8b5cf6);
  color: #fff;
  font-weight: 800;
  font-size: 15px;
  display: grid;
  place-items: center;
  letter-spacing: 0.5px;
  box-shadow: 0 6px 16px rgba(79, 110, 247, 0.35);
}
.company-id {
  font-size: 11px;
  color: var(--text-muted);
  font-weight: 600;
  padding: 3px 8px;
  background: #f1f5f9;
  border-radius: 6px;
  letter-spacing: 0.3px;
}
.company-name {
  margin: 0;
  font-size: 17px;
  font-weight: 700;
  letter-spacing: -0.3px;
}
.company-meta { display: flex; gap: 6px; flex-wrap: wrap; }
.company-actions {
  display: flex;
  gap: 8px;
  margin-top: 4px;
}
.company-actions .btn {
  flex: 1;
  padding: 8px 12px;
  font-size: 13px;
}

/* ============ Ratio cards ============ */
.ratio-card {
  position: relative;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px;
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  transition: all var(--transition);
}
.ratio-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}
.ratio-label {
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  margin-bottom: 8px;
}
.ratio-value {
  font-size: 24px;
  font-weight: 800;
  letter-spacing: -0.7px;
  margin-bottom: 12px;
}
.ratio-good { color: #10b981; }
.ratio-warn { color: #f59e0b; }
.ratio-bad { color: #ef4444; }
.ratio-neutral { color: var(--text-primary); }

.ratio-bar {
  height: 4px;
  background: #f1f5f9;
  border-radius: 999px;
  overflow: hidden;
}
.ratio-bar-fill {
  height: 100%;
  width: 100%;
  border-radius: 999px;
  animation: growBar 900ms cubic-bezier(0.4,0,0.2,1);
}
.ratio-fill-good { background: linear-gradient(90deg, #10b981, #34d399); }
.ratio-fill-warn { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.ratio-fill-bad { background: linear-gradient(90deg, #ef4444, #f87171); }
.ratio-fill-neutral { background: linear-gradient(90deg, #4f6ef7, #8b5cf6); }

@keyframes growBar {
  from { transform: scaleX(0); transform-origin: left; }
  to { transform: scaleX(1); transform-origin: left; }
}

/* ============ Score card (analysis / reports hero) ============ */
.score-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 28px;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 32px;
  align-items: center;
  box-shadow: var(--shadow-sm);
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
}
.score-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 4px;
  background: linear-gradient(90deg, #4f6ef7, #8b5cf6, #ec4899, #f59e0b);
}
.score-card-left {
  min-width: 0;
}
.score-card-label {
  font-size: 18px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.4px;
}
.score-card-right {
  flex-shrink: 0;
}

/* ============ Recommendations ============ */
.recommendation {
  position: relative;
  padding: 14px 18px 14px 48px;
  background: linear-gradient(135deg, #eff6ff 0%, #f5f3ff 100%);
  border-left: 3px solid var(--accent);
  border-radius: 10px;
  margin-bottom: 10px;
  font-size: 14px;
  color: var(--text-primary);
  line-height: 1.55;
  transition: all var(--transition);
}
.recommendation:hover {
  transform: translateX(3px);
  box-shadow: var(--shadow-sm);
}
.rec-num {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  display: grid;
  place-items: center;
  box-shadow: 0 2px 6px rgba(79, 110, 247, 0.35);
}

/* ============ Empty state ============ */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-muted);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}
.empty-state svg { opacity: 0.6; margin-bottom: 8px; }
.empty-state h3 {
  margin: 0;
  color: var(--text-primary);
  font-size: 18px;
  font-weight: 700;
}
.empty-state p { margin: 0; max-width: 400px; }

/* ============ Skeleton ============ */
.skeleton {
  background: linear-gradient(90deg, #f1f5f9 0%, #e2e8f0 50%, #f1f5f9 100%);
  background-size: 200% 100%;
  border-radius: 8px;
  animation: shimmer 1.4s infinite;
}
@keyframes shimmer {
  from { background-position: 200% 0; }
  to { background-position: -200% 0; }
}
.skeleton-card { padding: 24px; }

/* ============ Auth pages ============ */
.auth-shell {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
  background:
    radial-gradient(ellipse 80% 60% at 50% 0%, rgba(79, 110, 247, 0.25), transparent),
    radial-gradient(ellipse 60% 50% at 80% 100%, rgba(139, 92, 246, 0.18), transparent),
    linear-gradient(135deg, #0b1120 0%, #0f172a 50%, #1e1b4b 100%);
  position: relative;
  overflow: hidden;
}
.auth-shell::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
}
.auth-card {
  width: 100%;
  max-width: 440px;
  background: rgba(255, 255, 255, 0.98);
  padding: 40px;
  border-radius: var(--radius-xl);
  box-shadow:
    0 24px 64px rgba(0, 0, 0, 0.35),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 1;
  animation: fadeInUp 400ms cubic-bezier(0.4, 0, 0.2, 1);
}
.auth-card h1 {
  margin: 0 0 8px;
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.6px;
  background: linear-gradient(135deg, #0f172a, #4f6ef7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.auth-card p.muted { color: var(--text-secondary); margin: 0 0 28px; font-size: 14px; }

/* ============ Messages ============ */
.error {
  background: var(--danger-soft);
  color: #991b1b;
  padding: 12px 14px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 14px;
  border-left: 3px solid var(--danger);
}
.success {
  background: var(--success-soft);
  color: #065f46;
  padding: 12px 14px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 14px;
  border-left: 3px solid var(--success);
}

/* ============ Utility ============ */
.muted { color: var(--text-muted); }

::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
  border: 2px solid var(--bg-page);
}
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

/* ============ Responsive ============ */
@media (max-width: 900px) {
  .score-card { grid-template-columns: 1fr; text-align: center; }
  .score-card-right { justify-self: center; }
}

@media (max-width: 768px) {
  .sidebar { width: 76px; padding: 20px 10px; }
  .sidebar .brand { font-size: 0; padding: 0; justify-content: center; }
  .sidebar .brand::before { width: 36px; height: 36px; }
  .nav-section-label { display: none; }
  .sidebar a { justify-content: center; font-size: 0; padding: 12px; }
  .sidebar a .nav-icon { font-size: 18px; }
  .sidebar-footer .user-meta, .sidebar-footer .btn-ghost { display: none; }
  .topbar { padding: 0 16px; }
  .content { padding: 20px 16px; }
  .page-title { font-size: 22px; }
  .hero-title { font-size: 24px; }
}
'''

# =====================================================
# Write all files
# =====================================================
def main():
    count = 0
    for rel_path, content in FILES.items():
        p = ROOT / rel_path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content.lstrip("\\n"), encoding="utf-8")
        count += 1
        print(f"  updated  src/{rel_path}")
    print(f"\\nDone. {count} files updated.")


if __name__ == "__main__":
    main()