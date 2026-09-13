"""Add Plotly chart + model comparison UI."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "src"
FILES = {}

# =====================================================
# components/PlotlyChart.jsx
# =====================================================
FILES["components/PlotlyChart.jsx"] = '''
import Plot from "react-plotly.js";

export default function PlotlyChart({ values = [], title = "Cash Flow Forecast" }) {
  const x = values.map((_, i) => `Period +${i + 1}`);

  return (
    <Plot
      data={[
        {
          x,
          y: values,
          type: "scatter",
          mode: "lines+markers",
          marker: {
            color: "#a5b4fc",
            size: 10,
            line: { color: "#4f6ef7", width: 2 },
          },
          line: { color: "#8b5cf6", width: 3, shape: "spline" },
          fill: "tozeroy",
          fillcolor: "rgba(139, 92, 246, 0.15)",
        },
      ]}
      layout={{
        title: { text: title, font: { color: "#f1f5f9", size: 16 } },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        font: { color: "#cbd5e1" },
        xaxis: { gridcolor: "rgba(255,255,255,0.06)" },
        yaxis: { gridcolor: "rgba(255,255,255,0.06)" },
        margin: { l: 60, r: 20, t: 50, b: 40 },
        height: 320,
      }}
      config={{ displayModeBar: false, responsive: true }}
      style={{ width: "100%" }}
    />
  );
}
'''

# =====================================================
# components/ModelComparison.jsx
# =====================================================
FILES["components/ModelComparison.jsx"] = '''
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export default function ModelComparison({ data }) {
  if (!data?.models) return null;

  const rows = [];
  Object.entries(data.models).forEach(([modelName, modelData]) => {
    const predictions = modelData.predictions || modelData?.models?.random_forest?.predictions;
    if (predictions?.length) {
      predictions.forEach((val, i) => {
        rows.push({
          period: `+${i + 1}`,
          model: modelName,
          value: Number(val),
        });
      });
    }
  });

  if (!rows.length) return <p className="muted">No comparison data available.</p>;

  // pivot: one row per period with columns per model
  const periods = [...new Set(rows.map((r) => r.period))];
  const models = [...new Set(rows.map((r) => r.model))];
  const chartData = periods.map((p) => {
    const row = { period: p };
    models.forEach((m) => {
      const found = rows.find((r) => r.period === p && r.model === m);
      row[m] = found?.value ?? 0;
    });
    return row;
  });

  const colors = ["#a5b4fc", "#ec4899", "#10b981", "#f59e0b"];

  return (
    <ResponsiveContainer width="100%" height={320}>
      <BarChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
        <XAxis dataKey="period" stroke="#94a3b8" />
        <YAxis stroke="#94a3b8" />
        <Tooltip
          contentStyle={{
            background: "rgba(15,23,42,0.95)",
            border: "1px solid rgba(255,255,255,0.1)",
            borderRadius: 8,
            color: "#fff",
          }}
          formatter={(v) => Number(v).toLocaleString()}
        />
        <Legend />
        {models.map((m, i) => (
          <Bar key={m} dataKey={m} fill={colors[i % colors.length]} radius={[6, 6, 0, 0]} />
        ))}
      </BarChart>
    </ResponsiveContainer>
  );
}
'''

# =====================================================
# api/client.js — add LSTM/Prophet/compare
# =====================================================
ADDITIONS = '''
// ---------- Advanced ML models ----------
export const predictLSTM = (companyId, horizon = 3) =>
  api.get(`/advanced/predict/lstm/${companyId}?horizon=${horizon}`);

export const predictProphet = (companyId, horizon = 3) =>
  api.get(`/advanced/predict/prophet/${companyId}?horizon=${horizon}`);

export const compareModels = (companyId) =>
  api.get(`/advanced/compare/${companyId}`);
'''

path_client = ROOT / "api" / "client.js"
src = path_client.read_text(encoding="utf-8")
if "predictLSTM" not in src:
    path_client.write_text(src + ADDITIONS, encoding="utf-8")
    print("  updated  src/api/client.js")

# =====================================================
# pages/Predictions.jsx — add model comparison panel
# =====================================================
FILES["pages/Predictions.jsx"] = '''
import { useEffect, useState } from "react";

import {
  compareModels,
  listCompanies,
  predictCashflow,
  predictLSTM,
  predictProphet,
} from "../api/client";
import CashFlowChart from "../components/CashFlowChart";
import PlotlyChart from "../components/PlotlyChart";
import ModelComparison from "../components/ModelComparison";
import { IconTrending, IconBolt, IconSparkles } from "../components/Icons";

const MODELS = [
  { key: "random_forest", label: "Random Forest", fn: predictCashflow },
  { key: "lstm", label: "LSTM (Deep Learning)", fn: predictLSTM },
  { key: "prophet", label: "Prophet (Time Series)", fn: predictProphet },
];

export default function Predictions() {
  const [companies, setCompanies] = useState([]);
  const [companyId, setCompanyId] = useState("");
  const [horizon, setHorizon] = useState(3);
  const [activeModel, setActiveModel] = useState("random_forest");
  const [result, setResult] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [loading, setLoading] = useState(false);
  const [comparisonLoading, setComparisonLoading] = useState(false);
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
      const model = MODELS.find((m) => m.key === activeModel);
      const { data } = await model.fn(companyId, horizon);
      setResult({ ...data, model_key: activeModel });
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  const runComparison = async () => {
    setComparisonLoading(true);
    setError("");
    try {
      const { data } = await compareModels(companyId);
      setComparison(data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setComparisonLoading(false);
    }
  };

  const values =
    result?.predictions || result?.predicted_values || [];

  return (
    <div>
      <div className="page-header">
        <div className="page-icon" style={{ background: "linear-gradient(135deg,#8b5cf6,#ec4899)" }}>
          <IconTrending size={22} />
        </div>
        <div>
          <h2 className="page-title">AI Cash Flow Prediction</h2>
          <p className="page-subtitle">Compare Random Forest, LSTM, and Prophet models</p>
        </div>
      </div>

      <div className="card">
        <div className="grid grid-3" style={{ alignItems: "end" }}>
          <div>
            <label>Company</label>
            <select value={companyId} onChange={(e) => setCompanyId(e.target.value)}>
              {companies.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>
          <div>
            <label>Horizon (periods)</label>
            <input
              type="number" min="1" max="12" value={horizon}
              onChange={(e) => setHorizon(Number(e.target.value))}
            />
          </div>
          <button onClick={run} disabled={loading || !companyId}>
            <IconBolt size={16} />
            {loading ? "Running…" : "Predict"}
          </button>
        </div>

        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 16 }}>
          {MODELS.map((m) => (
            <button
              key={m.key}
              onClick={() => setActiveModel(m.key)}
              className={activeModel === m.key ? "" : "btn-ghost-dark"}
              style={{ fontSize: 13, padding: "8px 14px" }}
            >
              {m.label}
            </button>
          ))}
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      {loading && <div className="card"><div className="skeleton" style={{ height: 300 }} /></div>}

      {result && values.length > 0 && (
        <>
          <div className="stats-strip">
            <div className="stat-tile">
              <div className="stat-tile-icon" style={{ background: "linear-gradient(135deg,#4f6ef7,#6366f1)" }}>
                <IconBolt size={20} />
              </div>
              <div>
                <div className="stat-tile-label">Model</div>
                <div className="stat-tile-value" style={{ fontSize: 16 }}>
                  {result.model || result.model_name || activeModel}
                </div>
              </div>
            </div>
            <div className="stat-tile">
              <div className="stat-tile-icon" style={{ background: "linear-gradient(135deg,#10b981,#059669)" }}>
                <IconTrending size={20} />
              </div>
              <div>
                <div className="stat-tile-label">Next Period</div>
                <div className="stat-tile-value" style={{ fontSize: 18 }}>
                  {Number(values[0]).toLocaleString()}
                </div>
              </div>
            </div>
            {result.confidence !== undefined && (
              <div className="stat-tile">
                <div className="stat-tile-icon" style={{ background: "linear-gradient(135deg,#f59e0b,#ef4444)" }}>
                  <IconTrending size={20} />
                </div>
                <div>
                  <div className="stat-tile-label">Confidence</div>
                  <div className="stat-tile-value">{(result.confidence * 100).toFixed(0)}%</div>
                </div>
              </div>
            )}
          </div>

          <div className="card">
            <h3 className="card-title">Recharts View</h3>
            <CashFlowChart values={values} />
          </div>

          <div className="card">
            <h3 className="card-title">Plotly Interactive View</h3>
            <PlotlyChart values={values} />
          </div>
        </>
      )}

      <div className="card">
        <div className="card-header">
          <div className="header-icon-wrap" style={{ background: "linear-gradient(135deg,#8b5cf6,#ec4899)" }}>
            <IconSparkles size={18} />
          </div>
          <div>
            <h3 className="card-title">Compare All Models</h3>
            <p className="card-subtitle">See Random Forest vs LSTM vs Prophet side by side</p>
          </div>
        </div>
        <button onClick={runComparison} disabled={comparisonLoading || !companyId} style={{ marginTop: 12 }}>
          {comparisonLoading ? "Training models… (this may take 30–60s)" : "Run Comparison"}
        </button>

        {comparison && (
          <div style={{ marginTop: 20 }}>
            <ModelComparison data={comparison} />
            <table style={{ marginTop: 20 }}>
              <thead>
                <tr>
                  <th>Model</th>
                  <th>Next Period</th>
                  <th>Last Period</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(comparison.models).map(([name, m]) => {
                  const preds = m.predictions || m?.models?.random_forest?.predictions || [];
                  return (
                    <tr key={name}>
                      <td style={{ textTransform: "capitalize" }}>{name.replace("_", " ")}</td>
                      <td><strong>{preds[0] ? Number(preds[0]).toLocaleString() : "—"}</strong></td>
                      <td>{preds[preds.length - 1] ? Number(preds[preds.length - 1]).toLocaleString() : "—"}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
'''

# ---------- Write files ----------
for rel, content in FILES.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.lstrip("\n"), encoding="utf-8")
    print(f"  created  src/{rel}")

print("\n✅ Frontend tech-stack files added.")