
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
