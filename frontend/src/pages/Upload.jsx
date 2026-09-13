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
    const blob = new Blob([headers + "\n" + row + "\n"], { type: "text/csv" });
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
