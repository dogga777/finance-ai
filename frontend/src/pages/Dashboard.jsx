import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { createCompany, listCompanies } from "../api/client";
import Hero3D from "../components/Hero3D";
import {
  IconBuilding,
  IconPlus,
  IconSparkles,
  IconTrending,
  IconShield,
} from "../components/Icons";
import { useTilt } from "../hooks/useTilt";

function CompanyCard({ company }) {
  const { ref, style, onMouseMove, onMouseLeave } = useTilt({ max: 6, scale: 1.03 });

  return (
    <div
      ref={ref}
      className="company-card"
      style={style}
      onMouseMove={onMouseMove}
      onMouseLeave={onMouseLeave}
    >
      <div className="company-card-top">
        <div className="company-avatar">
          {company.name.slice(0, 2).toUpperCase()}
        </div>
        <div className="company-id">ID #{company.id}</div>
      </div>
      <h3 className="company-name">{company.name}</h3>
      <div className="company-meta">
        <span className="chip">{company.industry}</span>
        <span className="chip">{company.currency}</span>
      </div>
      <div className="company-actions">
        <Link className="btn" to={`/upload?company=${company.id}`}>
          Upload Data
        </Link>
        <Link className="btn btn-ghost-dark" to="/analysis">
          Analyze
        </Link>
      </div>
    </div>
  );
}

export default function Dashboard() {
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
      {/* ---------- 3D Hero ---------- */}
      <div className="hero-3d">
        <div className="hero-3d-content">
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
        <div className="hero-3d-scene">
          <Hero3D />
        </div>
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
            <CompanyCard key={c.id} company={c} />
          ))}
        </div>
      )}
    </div>
  );
}
