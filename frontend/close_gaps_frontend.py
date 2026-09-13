"""FinSight AI — Close critical frontend gaps."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

FILES = {}

# =====================================================
# api/client.js — add advanced endpoints
# =====================================================
CLIENT_ADDITIONS = '''
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
'''

path_client = SRC / "api" / "client.js"
client_src = path_client.read_text(encoding="utf-8")
if "advancedPredict" not in client_src:
    path_client.write_text(client_src + "\n" + CLIENT_ADDITIONS, encoding="utf-8")
    print("  updated  src/api/client.js")

# =====================================================
# utils/excel.js — parse xlsx client-side
# =====================================================
FILES["utils/excel.js"] = '''
import * as XLSX from "xlsx";

const NUMERIC = [
  "revenue", "expenses", "assets", "liabilities", "equity",
  "inventory", "operating_cash_flow", "investing_cash_flow",
  "financing_cash_flow", "net_profit",
];

export async function parseExcelFile(file) {
  const buf = await file.arrayBuffer();
  const wb = XLSX.read(buf, { type: "array" });
  const sheet = wb.Sheets[wb.SheetNames[0]];
  const rows = XLSX.utils.sheet_to_json(sheet, { defval: 0 });

  if (!rows.length) throw new Error("Excel sheet is empty");

  return rows.map((r, i) => {
    const norm = {};
    Object.keys(r).forEach((k) => {
      norm[k.trim().toLowerCase()] = r[k];
    });

    if (!norm.period) throw new Error(`Row ${i + 2}: missing "period" column`);
    const obj = { period: String(norm.period).trim() };
    NUMERIC.forEach((f) => {
      const v = norm[f];
      obj[f] = v === "" || v === undefined ? 0 : Number(v);
      if (Number.isNaN(obj[f])) {
        throw new Error(`Row ${i + 2}: "${f}" is not a number (got "${v}")`);
      }
    });
    return obj;
  });
}
'''

# =====================================================
# components/TrendsChart.jsx — historical trends
# =====================================================
FILES["components/TrendsChart.jsx"] = '''
import {
  CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from "recharts";

export default function TrendsChart({ trends, metric }) {
  if (!trends?.periods?.length) return null;

  const data = trends.periods.map((p, i) => ({
    period: p,
    value: trends[metric]?.[i] ?? 0,
  }));

  return (
    <ResponsiveContainer width="100%" height={240}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
        <XAxis dataKey="period" stroke="#94a3b8" fontSize={12} />
        <YAxis stroke="#94a3b8" fontSize={12} />
        <Tooltip
          contentStyle={{
            background: "rgba(15,23,42,0.95)",
            border: "1px solid rgba(255,255,255,0.1)",
            borderRadius: 8,
            color: "#fff",
          }}
          formatter={(v) => Number(v).toLocaleString()}
        />
        <Line type="monotone" dataKey="value" stroke="#a5b4fc" strokeWidth={2.5} dot={{ r: 3 }} />
      </LineChart>
    </ResponsiveContainer>
  );
}
'''

# =====================================================
# pages/Upload.jsx — Excel + CSV support
# =====================================================
FILES["pages/Upload.jsx"] = '''
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

import { bulkUploadStatements, listCompanies, listStatements, uploadExcel } from "../api/client";
import { parseCSV, rowsToStatements } from "../utils/csv";
import { parseExcelFile } from "../utils/excel";
import { IconUpload, IconFile, IconDownload, IconRefresh } from "../components/Icons";

export default function Upload() {
  const [params] = useSearchParams();
  const [companies, setCompanies] = useState([]);
  const [companyId, setCompanyId] = useState(params.get("company") || "");
  const [statements, setStatements] = useState([]);
  const [fileName, setFileName] = useState("");
  const [parsedRows, setParsedRows] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [uploading, setUploading] = useState(false);

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

  const readFile = async (file) => {
    if (!file) return;
    setError("");
    setMessage("");
    setFileName(file.name);

    const lower = file.name.toLowerCase();
    try {
      if (lower.endsWith(".csv")) {
        const text = await file.text();
        const rows = parseCSV(text);
        if (!rows.length) throw new Error("CSV file has no data rows");
        setParsedRows(rowsToStatements(rows));
      } else if (lower.endsWith(".xlsx") || lower.endsWith(".xls")) {
        const statements = await parseExcelFile(file);
        setParsedRows(statements);
      } else {
        throw new Error("Please upload a .csv, .xlsx, or .xls file");
      }
    } catch (err) {
      setError(err.message);
      setParsedRows(null);
    }
  };

  const onFileChange = (e) => readFile(e.target.files?.[0]);
  const onDrop = (e) => { e.preventDefault(); setDragOver(false); readFile(e.dataTransfer.files?.[0]); };
  const onDragOver = (e) => { e.preventDefault(); setDragOver(true); };
  const onDragLeave = () => setDragOver(false);

  const upload = async () => {
    if (!parsedRows || !companyId) return;
    setUploading(true);
    setError("");
    setMessage("");
    try {
      const file = document.querySelector('input[type="file"]')?.files?.[0];
      if (file && (file.name.endsWith(".xlsx") || file.name.endsWith(".xls"))) {
        const r = await uploadExcel(companyId, file);
        setMessage(`✅ Uploaded ${r.data.count} statements from Excel`);
      } else {
        await bulkUploadStatements(companyId, parsedRows);
        setMessage(`✅ Uploaded ${parsedRows.length} statements`);
      }
      setParsedRows(null);
      setFileName("");
      const { data } = await listStatements(companyId);
      setStatements(data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setUploading(false);
    }
  };

  const downloadTemplate = () => {
    const headers = "period,revenue,expenses,assets,liabilities,equity,inventory,operating_cash_flow,investing_cash_flow,financing_cash_flow,net_profit";
    const row = "2024-01,100000,70000,500000,200000,300000,50000,25000,-10000,5000,20000";
    const blob = new Blob([headers + "\\n" + row + "\\n"], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "finsight_template.csv";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div>
      <div className="page-header">
        <div className="page-icon" style={{ background: "linear-gradient(135deg,#4f6ef7,#6366f1)" }}>
          <IconUpload size={22} />
        </div>
        <div>
          <h2 className="page-title">Upload Financial Data</h2>
          <p className="page-subtitle">Drop a CSV or Excel file — we'll parse it automatically</p>
        </div>
      </div>

      <div className="card">
        <label>Select Company</label>
        <select value={companyId} onChange={(e) => setCompanyId(e.target.value)}>
          <option value="">— choose —</option>
          {companies.map((c) => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </select>
      </div>

      <div className="card">
        <div className="card-header">
          <div className="header-icon-wrap" style={{ background: "linear-gradient(135deg,#8b5cf6,#ec4899)" }}>
            <IconFile size={18} />
          </div>
          <div>
            <h3 className="card-title">Upload File</h3>
            <p className="card-subtitle">.csv, .xlsx, .xls supported</p>
          </div>
        </div>

        <div
          className={`dropzone ${dragOver ? "dropzone-active" : ""}`}
          onDrop={onDrop}
          onDragOver={onDragOver}
          onDragLeave={onDragLeave}
          onClick={() => document.getElementById("fileInput").click()}
        >
          <div className="dropzone-icon"><IconUpload size={32} /></div>
          <div className="dropzone-title">
            {fileName ? fileName : "Drop your file here or click to browse"}
          </div>
          <div className="dropzone-hint">CSV or Excel · max 5 MB</div>
          <input
            id="fileInput"
            type="file"
            accept=".csv,.xlsx,.xls,text/csv,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            onChange={onFileChange}
            style={{ display: "none" }}
          />
        </div>

        <div className="upload-actions">
          <button onClick={upload} disabled={!parsedRows || !companyId || uploading}>
            <IconUpload size={16} />
            {uploading ? "Uploading…" : "Upload"}
          </button>
          <button onClick={downloadTemplate} className="btn-ghost-dark">
            <IconDownload size={16} />
            Download Template
          </button>
          {parsedRows && (
            <button
              onClick={() => { setParsedRows(null); setFileName(""); }}
              className="btn-ghost-dark"
            >
              <IconRefresh size={16} /> Clear
            </button>
          )}
        </div>

        {error && <div className="error" style={{ marginTop: 12 }}>{error}</div>}
        {message && <div className="success" style={{ marginTop: 12 }}>{message}</div>}
      </div>

      {parsedRows && (
        <div className="card">
          <h3 className="card-title">Preview · {parsedRows.length} rows</h3>
          <div style={{ overflowX: "auto", marginTop: 12 }}>
            <table>
              <thead>
                <tr>
                  <th>Period</th><th>Revenue</th><th>Expenses</th>
                  <th>Assets</th><th>Liabilities</th><th>Net Profit</th><th>Operating CF</th>
                </tr>
              </thead>
              <tbody>
                {parsedRows.slice(0, 20).map((s, i) => (
                  <tr key={i}>
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
        </div>
      )}

      <div className="card">
        <h3 className="card-title">Existing Statements ({statements.length})</h3>
        {statements.length > 0 && (
          <div style={{ overflowX: "auto", marginTop: 12 }}>
            <table>
              <thead>
                <tr>
                  <th>Period</th><th>Revenue</th><th>Expenses</th>
                  <th>Assets</th><th>Liabilities</th><th>Net Profit</th><th>Operating CF</th>
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
        )}
      </div>
    </div>
  );
}
'''

# =====================================================
# pages/Analysis.jsx — add trends + text explanation
# =====================================================
FILES["pages/Analysis.jsx"] = '''
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
'''

# =====================================================
# pages/Reports.jsx — add Excel download
# =====================================================
path_reports = SRC / "pages" / "Reports.jsx"
reports_src = path_reports.read_text(encoding="utf-8")

if "downloadExcelReport" not in reports_src:
    # Add import
    reports_src = reports_src.replace(
        'import { downloadReportPdf, getReport, listCompanies } from "../api/client";',
        'import { downloadReportPdf, downloadExcelReport, getReport, listCompanies } from "../api/client";'
    )
    # Add excel handler after downloadPdf function
    excel_handler = '''
  const downloadExcel = async () => {
    try {
      const { data } = await downloadExcelReport(companyId);
      const url = URL.createObjectURL(new Blob([data], {
        type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
      }));
      const a = document.createElement("a");
      a.href = url;
      a.download = `finsight_report_${companyId}.xlsx`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      setError("Excel download failed");
    }
  };
'''
    reports_src = reports_src.replace(
        "  return (\n    <div>\n      <div className=\"page-header\">",
        excel_handler + "\n  return (\n    <div>\n      <div className=\"page-header\">"
    )
    # Add button next to PDF button
    reports_src = reports_src.replace(
        '''<button onClick={downloadPdf} className="btn-success">
              <IconDownload size={16} />
              Download PDF
            </button>''',
        '''<button onClick={downloadPdf} className="btn-success">
              <IconDownload size={16} />
              Download PDF
            </button>
            <button onClick={downloadExcel} className="btn-success">
              <IconDownload size={16} />
              Download Excel
            </button>'''
    )
    path_reports.write_text(reports_src, encoding="utf-8")
    print("  updated  src/pages/Reports.jsx")

# ---------- Write all new files ----------
for rel, content in FILES.items():
    p = SRC / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.lstrip("\n"), encoding="utf-8")
    print(f"  created  src/{rel}")

print("\n✅ Frontend gap-closing script complete.")