import { useTilt } from "../hooks/useTilt";

export default function RatioCard({ label, value, suffix = "" }) {
  const display = typeof value === "number" ? value.toFixed(4) : value ?? "—";

  let trend = "neutral";
  if (typeof value === "number") {
    if (label.toLowerCase().includes("debt")) {
      trend = value < 0.5 ? "good" : value < 0.7 ? "warn" : "bad";
    } else {
      trend = value > 0 ? "good" : "bad";
    }
  }

  const { ref, style, onMouseMove, onMouseLeave } = useTilt({ max: 10, scale: 1.05 });

  return (
    <div
      ref={ref}
      className="ratio-card"
      style={style}
      onMouseMove={onMouseMove}
      onMouseLeave={onMouseLeave}
    >
      <div className="ratio-label">{label}</div>
      <div className={`ratio-value ratio-${trend}`}>
        {display}
        {suffix}
      </div>
      <div className="ratio-bar">
        <div className={`ratio-bar-fill ratio-fill-${trend}`} />
      </div>
    </div>
  );
}
