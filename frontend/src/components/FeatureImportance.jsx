import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export default function FeatureImportance({ data = {} }) {
  const chartData = Object.entries(data)
    .filter(([k]) => k !== "error")
    .map(([feature, importance]) => ({ feature, importance: Number(importance) }));

  if (!chartData.length) {
    return <p className="muted">No feature importance data available.</p>;
  }

  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
        <XAxis dataKey="feature" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="importance" fill="#2563eb" radius={[6, 6, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
