"""FinSight AI — CSV upload upgrade."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
PUBLIC = ROOT / "public"

FILES = {}

# =====================================================
# utils/csv.js — small, dependency-free CSV parser
# =====================================================
FILES["src/utils/csv.js"] = '''
/**
 * Parse a CSV string into an array of objects.
 * Handles quoted fields, commas inside quotes, CRLF/LF.
 */
export function parseCSV(text) {
  const rows = [];
  let row = [];
  let field = "";
  let inQuotes = false;
  let i = 0;

  // strip BOM
  if (text.charCodeAt(0) === 0xfeff) text = text.slice(1);

  while (i < text.length) {
    const ch = text[i];

    if (inQuotes) {
      if (ch === '"') {
        if (text[i + 1] === '"') {
          field += '"';
          i += 2;
          continue;
        }
        inQuotes = false;
        i++;
        continue;
      }
      field += ch;
      i++;
      continue;
    }

    if (ch === '"') {
      inQuotes = true;
      i++;
      continue;
    }

    if (ch === ",") {
      row.push(field);
      field = "";
      i++;
      continue;
    }

    if (ch === "\\n") {
      row.push(field);
      rows.push(row);
      row = [];
      field = "";
      i++;
      continue;
    }

    if (ch === "\\r") {
      i++;
      continue;
    }

    field += ch;
    i++;
  }

  // last cell
  if (field.length > 0 || row.length > 0) {
    row.push(field);
    rows.push(row);
  }

  if (rows.length === 0) return [];

  const headers = rows[0].map((h) => h.trim());
  const dataRows = rows.slice(1).filter((r) => r.some((c) => c.trim() !== ""));

  return dataRows.map((r) => {
    const obj = {};
    headers.forEach((h, idx) => {
      obj[h] = (r[idx] ?? "").trim();
    });
    return obj;
  });
}

/** Convert parsed CSV rows into Statement objects for the API. */
export function rowsToStatements(rows) {
  const NUMERIC = [
    "revenue", "expenses", "assets", "liabilities", "equity",
    "inventory", "operating_cash_flow", "investing_cash_flow",
    "financing_cash_flow", "net_profit",
  ];

  return rows.map((r, i) => {
    if (!r.period) {
      throw new Error(`Row ${i + 2}: missing "period" column`);
    }
    const obj = { period: String(r.period).trim() };
    NUMERIC.forEach((f) => {
      const v = r[f];
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
# pages/Upload.jsx — CSV-first experience
# =====================================================
FILES["src/pages/Upload.jsx"] = '''
import { useEffect, useMemo, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";

import { bulkUploadStatements, listCompanies, listStatements } from "../api/client";
import { parseCSV, rowsToStatements } from "../utils/csv";
import {
  IconUpload,
  IconFile,
  IconDownload,
  IconRefresh,
} from "../components/Icons";

const TEMPLATE_HEADERS = [
  "period", "revenue", "expenses", "assets", "liabilities",
  "equity", "inventory", "operating_cash_flow",
  "investing_cash_flow", "financing_cash_flow", "net_profit",
];

const TEMPLATE_ROWS = [
  ["2024-01", 100000, 70000, 500000, 200000, 300000, 50000, 25000, -10000, 5000, 20000],
  ["2024-02", 105000, 73000, 510000, 205000, 305000, 52000, 26000, -9000, 4000, 21000],
  ["2024-03",  98000, 75000, 505000, 210000, 295000, 55000, 22000, -11000, 6000, 18000],
  ["2024-04", 110000, 76000, 520000, 215000, 305000, 58000, 28000, -12000, 5000, 24000],
  ["2024-05", 115000, 80000, 540000, 220000, 320000, 60000, 30000, -10000, 4000, 25000],
  ["2024-06", 120000, 82000, 560000, 230000, 330000, 62000, 32000, -15000, 7000, 28000],
];

function buildTemplateCSV() {
  const head = TEMPLATE_HEADERS.join(",");
  const body = TEMPLATE_ROWS.map((r) => r.join(",")).join("\\n");
  return head + "\\n" + body + "\\n";
}

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

  const fileInputRef = useRef(null);

  // ---------- load companies + statements ----------
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

  // ---------- read CSV file ----------
  const readFile = (file) => {
    if (!file) return;
    if (!file.name.toLowerCase().endsWith(".csv")) {
      setError("Please upload a .csv file");
      return;
    }
    setError("");
    setMessage("");
    setFileName(file.name);

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const text = e.target.result;
        const rows = parseCSV(text);
        if (rows.length === 0) {
          setError("CSV file is empty or has no data rows");
          setParsedRows(null);
          return;
        }
        const statements = rowsToStatements(rows);
        setParsedRows(statements);
      } catch (err) {
        setError(err.message);
        setParsedRows(null);
      }
    };
    reader.readAsText(file);
  };

  const onFileChange = (e) => readFile(e.target.files?.[0]);

  const onDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    readFile(e.dataTransfer.files?.[0]);
  };

  const onDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const onDragLeave = () => setDragOver(false);

  // ---------- upload ----------
  const upload = async () => {
    if (!parsedRows || !companyId) return;
    setUploading(true);
    setError("");
    setMessage("");
    try {
      await bulkUploadStatements(companyId, parsedRows);
      setMessage(`✅ Uploaded ${parsedRows.length} statements successfully`);
      setParsedRows(null);
      setFileName("");
      if (fileInputRef.current) fileInputRef.current.value = "";
      const { data } = await listStatements(companyId);
      setStatements(data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setUploading(false);
    }
  };

  // ---------- download template ----------
  const downloadTemplate = () => {
    const csv = buildTemplateCSV();
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "finsight_sample_statements.csv";
    a.click();
    URL.revokeObjectURL(url);
  };

  // ---------- preview columns ----------
  const previewColumns = useMemo(() => TEMPLATE_HEADERS, []);

  return (
    <div>
      <div className="page-header">
        <div className="page-icon" style={{ background: "linear-gradient(135deg,#4f6ef7,#6366f1)" }}>
          <IconUpload size={22} />
        </div>
        <div>
          <h2 className="page-title">Upload Financial Statements</h2>
          <p className="page-subtitle">
            Drop a CSV file or download the template to get started
          </p>
        </div>
      </div>

      {/* ----- Company selector ----- */}
      <div className="card">
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

      {/* ----- Dropzone ----- */}
      <div className="card">
        <div className="card-header">
          <div className="header-icon-wrap" style={{ background: "linear-gradient(135deg,#8b5cf6,#ec4899)" }}>
            <IconFile size={18} />
          </div>
          <div>
            <h3 className="card-title">Upload CSV File</h3>
            <p className="card-subtitle">
              One row per period. Columns must match the template.
            </p>
          </div>
        </div>

        <div
          className={`dropzone ${dragOver ? "dropzone-active" : ""}`}
          onDrop={onDrop}
          onDragOver={onDragOver}
          onDragLeave={onDragLeave}
          onClick={() => fileInputRef.current?.click()}
        >
          <div className="dropzone-icon">
            <IconUpload size={32} />
          </div>
          <div className="dropzone-title">
            {fileName ? fileName : "Drop your CSV here or click to browse"}
          </div>
          <div className="dropzone-hint">
            Only .csv files · max 5 MB
          </div>
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv,text/csv"
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
            Download CSV Template
          </button>
          {parsedRows && (
            <button
              onClick={() => {
                setParsedRows(null);
                setFileName("");
                if (fileInputRef.current) fileInputRef.current.value = "";
              }}
              className="btn-ghost-dark"
            >
              <IconRefresh size={16} />
              Clear
            </button>
          )}
        </div>

        {error && <div className="error" style={{ marginTop: 12 }}>{error}</div>}
        {message && <div className="success" style={{ marginTop: 12 }}>{message}</div>}
      </div>

      {/* ----- Preview ----- */}
      {parsedRows && (
        <div className="card">
          <div className="card-header">
            <div>
              <h3 className="card-title">Preview · {parsedRows.length} rows</h3>
              <p className="card-subtitle">Verify before uploading</p>
            </div>
          </div>
          <div style={{ overflowX: "auto" }}>
            <table>
              <thead>
                <tr>
                  {previewColumns.map((c) => (
                    <th key={c}>{c}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {parsedRows.slice(0, 20).map((row, i) => (
                  <tr key={i}>
                    {previewColumns.map((c) => (
                      <td key={c}>
                        {typeof row[c] === "number"
                          ? row[c].toLocaleString()
                          : row[c]}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
            {parsedRows.length > 20 && (
              <p className="muted" style={{ padding: 12, fontSize: 13 }}>
                … and {parsedRows.length - 20} more rows
              </p>
            )}
          </div>
        </div>
      )}

      {/* ----- Existing statements ----- */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">Existing Statements ({statements.length})</h3>
            <p className="card-subtitle">Already stored for this company</p>
          </div>
        </div>
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

# =====================================================
# public/finsight_sample_statements.csv — sample file
# =====================================================
FILES["public/finsight_sample_statements.csv"] = """period,revenue,expenses,assets,liabilities,equity,inventory,operating_cash_flow,investing_cash_flow,financing_cash_flow,net_profit
2024-01,100000,70000,500000,200000,300000,50000,25000,-10000,5000,20000
2024-02,105000,73000,510000,205000,305000,52000,26000,-9000,4000,21000
2024-03,98000,75000,505000,210000,295000,55000,22000,-11000,6000,18000
2024-04,110000,76000,520000,215000,305000,58000,28000,-12000,5000,24000
2024-05,115000,80000,540000,220000,320000,60000,30000,-10000,4000,25000
2024-06,120000,82000,560000,230000,330000,62000,32000,-15000,7000,28000
2024-07,118000,81000,555000,225000,330000,63000,31000,-8000,5000,27000
2024-08,125000,84000,575000,235000,340000,65000,34000,-12000,6000,29000
2024-09,130000,86000,590000,240000,350000,68000,36000,-10000,7000,30000
2024-10,128000,85000,585000,238000,347000,67000,35000,-9000,4000,29000
2024-11,135000,88000,605000,245000,360000,70000,38000,-11000,5000,32000
2024-12,140000,90000,620000,250000,370000,72000,40000,-13000,8000,34000
"""

# =====================================================
# Append CSS for dropzone + upload actions
# =====================================================
CSS = '''

/* =====================================================
   CSV UPLOAD
   ===================================================== */

.dropzone {
  position: relative;
  margin-top: 14px;
  padding: 48px 24px;
  border-radius: var(--radius-lg);
  border: 2px dashed rgba(255, 255, 255, 0.12);
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.03) 0%,
    rgba(255, 255, 255, 0.01) 100%
  );
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  text-align: center;
  cursor: pointer;
  transition: all 220ms cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.dropzone::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    circle at 50% 0%,
    rgba(99, 102, 241, 0.15),
    transparent 60%
  );
  opacity: 0;
  transition: opacity 220ms ease;
  pointer-events: none;
}

.dropzone:hover {
  border-color: rgba(165, 180, 252, 0.35);
  background: linear-gradient(
    135deg,
    rgba(99, 102, 241, 0.06) 0%,
    rgba(139, 92, 246, 0.03) 100%
  );
  transform: translateY(-2px);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.06),
    0 12px 32px rgba(0, 0, 0, 0.3),
    0 0 40px rgba(99, 102, 241, 0.1);
}

.dropzone:hover::before { opacity: 1; }

.dropzone-active {
  border-color: rgba(165, 180, 252, 0.6);
  background: linear-gradient(
    135deg,
    rgba(99, 102, 241, 0.15) 0%,
    rgba(139, 92, 246, 0.08) 100%
  );
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.1),
    0 16px 40px rgba(0, 0, 0, 0.4),
    0 0 60px rgba(99, 102, 241, 0.25);
  transform: scale(1.01);
}

.dropzone-active::before { opacity: 1; }

.dropzone-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.12));
  border: 1px solid rgba(165, 180, 252, 0.22);
  color: #c7d2fe;
  margin-bottom: 16px;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.15),
    0 8px 24px rgba(99, 102, 241, 0.2);
}

.dropzone-title {
  font-size: 15px;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 4px;
}

.dropzone-hint {
  font-size: 12.5px;
  color: #64748b;
}

.upload-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 16px;
}
'''

path_css = SRC / "index.css"
existing = path_css.read_text(encoding="utf-8")

marker = "/* =====================================================\n   CSV UPLOAD"
if marker in existing:
    existing = existing.split(marker)[0].rstrip() + "\n"

path_css.write_text(existing + CSS, encoding="utf-8")
print("  updated  src/index.css (CSV section)")

# ---------- Write files ----------
for rel, content in FILES.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.lstrip("\n"), encoding="utf-8")
    print(f"  updated  {rel}")

print("\nDone. CSV upload installed.")