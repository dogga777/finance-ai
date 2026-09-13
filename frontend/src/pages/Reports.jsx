import { useEffect, useState } from "react";

import {
  downloadExcelReport,
  downloadReportPdf,
  getReport,
  listCompanies,
} from "../api/client";
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

  const downloadExcel = async () => {
    try {
      const { data } = await downloadExcelReport(companyId);
      const url = URL.createObjectURL(
        new Blob([data], {
          type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        })
      );
      const a = document.createElement("a");
      a.href = url;
      a.download = `finsight_report_${companyId}.xlsx`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      setError("Excel download failed");
    }
  };

  return (
    <div>
      <div className="page-header">
        <div
          className="page-icon"
          style={{ background: "linear-gradient(135deg,#10b981,#059669)" }}
        >
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
            <div style={{ display: "flex", gap: 8 }}>
              <button onClick={downloadPdf} className="btn-success" style={{ flex: 1 }}>
                <IconDownload size={16} />
                PDF
              </button>
              <button onClick={downloadExcel} className="btn-success" style={{ flex: 1 }}>
                <IconDownload size={16} />
                Excel
              </button>
            </div>
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
              <div
                className="header-icon-wrap"
                style={{ background: "linear-gradient(135deg,#f59e0b,#ef4444)" }}
              >
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
              <div
                className="header-icon-wrap"
                style={{ background: "linear-gradient(135deg,#8b5cf6,#ec4899)" }}
              >
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
                    <td>
                      <strong>{Number(v).toLocaleString()}</strong>
                    </td>
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