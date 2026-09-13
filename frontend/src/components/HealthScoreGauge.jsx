
export default function HealthScoreGauge({ score = 0, riskLevel = "Unknown" }) {
  const radius = 80;
  const circumference = Math.PI * radius;
  const progress = (Math.max(0, Math.min(100, score)) / 100) * circumference;

  const color =
    riskLevel === "Low" ? "#10b981" : riskLevel === "Medium" ? "#f59e0b" : "#ef4444";
  const gradId = "gauge-" + riskLevel.toLowerCase();

  return (
    <div style={{ textAlign: "center", padding: "6px 0" }}>
      <svg viewBox="0 0 200 120" width="280" height="170">
        <defs>
          <linearGradient id={gradId} x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor={color} stopOpacity="0.7" />
            <stop offset="100%" stopColor={color} />
          </linearGradient>
        </defs>
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke="#f1f5f9"
          strokeWidth="16"
          strokeLinecap="round"
        />
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke={`url(#${gradId})`}
          strokeWidth="16"
          strokeLinecap="round"
          strokeDasharray={`${progress} ${circumference}`}
          style={{ transition: "stroke-dasharray 800ms cubic-bezier(0.4,0,0.2,1)" }}
        />
        <text x="100" y="88" textAnchor="middle" fontSize="34" fontWeight="800" fill="#0f172a" letterSpacing="-1">
          {score}
        </text>
        <text x="100" y="108" textAnchor="middle" fontSize="12" fill="#94a3b8" fontWeight="500">
          OUT OF 100
        </text>
      </svg>
      <div style={{ marginTop: 4 }}>
        <span className={`badge ${riskLevel.toLowerCase()}`}>{riskLevel} Risk</span>
      </div>
    </div>
  );
}
