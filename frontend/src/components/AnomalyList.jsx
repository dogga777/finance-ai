export default function AnomalyList({ reasons = [], riskLevel = "Low" }) {
  return (
    <div>
      <div style={{ marginBottom: 14 }}>
        Risk Level:{" "}
        <span className={`badge ${riskLevel.toLowerCase()}`}>{riskLevel}</span>
      </div>
      {reasons.length === 0 ? (
        <p className="muted">No anomalies detected. Financial patterns look normal.</p>
      ) : (
        <ul style={{ paddingLeft: 20 }}>
          {reasons.map((reason, i) => (
            <li key={i} style={{ marginBottom: 8 }}>
              {reason}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
