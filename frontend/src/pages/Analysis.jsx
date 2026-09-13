import { useEffect, useState } from "react";

import { analyzeCompany, getTextExplanation, getTrends, listCompanies } from "../api/client";
import HealthScoreGauge from "../components/HealthScoreGauge";
import RatioCard from "../components/RatioCard";
import TrendsChart from "../components/TrendsChart";
import { IconChart, IconSparkles } from "../components/Icons";

const TREND_METRICS = [
  { key: "revenue", label: "Revenue" },
  { key: "expenses", label: "Expenses" },
  { key: "net_profit", label: "Net Profit" },
  { key: "operating_cash_flow", label: "Operating Cash Flow" },
  { key: "current_ratio", label: "Current Ratio" },
  { key: "net_margin", label: "Net Profit Margin" },
];

export default function Analysis() {
  const [companies, setCompanies] = useState([]);
  const [companyId, setCompanyId] = useState("");
  const [result, setResult] = useState(null);
  const [trends, setTrends] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [activeTrend, setActiveTrend] = useState("revenue");
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
    setTrends(null);
    setExplanation(null);

    Promise.all([
      analyzeCompany(companyId).catch(() => null),
      getTrends(companyId).catch(() => null),
      getTextExplanation(companyId).catch(() => null),
    ])
      .then(([analysis, trendsRes, explRes]) => {
        if (analysis) setResult(analysis.data);
        if (trendsRes) setTrends(trendsRes.data);
        if (explRes) setExplanation(explRes.data);
        if (!analysis) setError("No data — upload statements first");
      })
      .finally(() => setLoading(false));
  }, [companyId]);

  return (
    <div>
      <div className="page-header">
        <div className="page-icon" style={{ background: "linear-gradient(135deg,#4f6ef7,#6366f1)" }}>
          <IconChart size={22} />
        </div>
        <div>
          <h2 className="page-title">Financial Analysis</h2>
          <p className="page-subtitle">Ratios, trends, and AI-generated insights</p>
        </div>
      </div>

      <div className="card">
        <label>Select Company</label>
        <select value={companyId} onChange={(e) => setCompanyId(e.target.value)}>
          {companies.map((c) => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </select>
      </div>

      {error && <div className="error">{error}</div>}
      {loading && <div className="card"><div className="skeleton" style={{ height: 200 }} /></div>}

      {result && (
        <>
          <div className="score-card">
            <div className="score-card-left">
              <div className="score-card-label">Financial Health Score</div>
              <p className="muted" style={{ margin: "4px 0 0" }}>
                Computed from 7 financial ratios using weighted scoring
              </p>
            </div>
            <div className="score-card-right">
              <HealthScoreGauge score={result.score.score} riskLevel={result.score.risk_level} />
            </div>
          </div>

          {explanation && (
            <div className="card">
              <div className="card-header">
                <div className="header-icon-wrap" style={{ background: "linear-gradient(135deg,#8b5cf6,#ec4899)" }}>
                  <IconSparkles size={18} />
                </div>
                <div>
                  <h3 className="card-title">AI Explanation</h3>
                  <p className="card-subtitle">Natural language summary of current position</p>
                </div>
              </div>
              <p style={{ lineHeight: 1.7, marginTop: 12 }}>{explanation.summary}</p>
              {explanation.drivers?.length > 0 && (
                <div style={{ marginTop: 12 }}>
                  {explanation.drivers.map((d, i) => (
                    <div key={i} style={{ display: "flex", justifyContent: "space-between", padding: "8px 0", borderTop: "1px solid rgba(255,255,255,0.05)" }}>
                      <span style={{ textTransform: "capitalize", color: "#cbd5e1" }}>{d.factor}</span>
                      <span className={`badge ${d.impact === "positive" ? "low" : d.impact === "negative" ? "high" : "medium"}`}>
                        {d.impact}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          <div className="section-heading">
            <h3>Trend Analysis</h3>
            <span className="muted" style={{ fontSize: 13 }}>Historical performance over time</span>
          </div>

          <div className="card">
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 16 }}>
              {TREND_METRICS.map((m) => (
                <button
                  key={m.key}
                  onClick={() => setActiveTrend(m.key)}
                  className={activeTrend === m.key ? "" : "btn-ghost-dark"}
                  style={{ fontSize: 13, padding: "6px 12px" }}
                >
                  {m.label}
                </button>
              ))}
            </div>
            <TrendsChart trends={trends} metric={activeTrend} />
          </div>

          <div className="section-heading"><h3>Financial Ratios</h3></div>
          <div className="grid grid-4">
            <RatioCard label="Current Ratio" value={result.ratios.current_ratio} />
            <RatioCard label="Quick Ratio" value={result.ratios.quick_ratio} />
            <RatioCard label="Debt Ratio" value={result.ratios.debt_ratio} />
            <RatioCard label="ROA" value={result.ratios.roa} />
            <RatioCard label="ROE" value={result.ratios.roe} />
            <RatioCard label="Gross Margin" value={result.ratios.gross_margin} />
            <RatioCard label="Net Profit Margin" value={result.ratios.net_profit_margin} />
          </div>
        </>
      )}
    </div>
  );
}
