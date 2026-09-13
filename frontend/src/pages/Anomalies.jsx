import { useEffect, useState } from "react";

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
