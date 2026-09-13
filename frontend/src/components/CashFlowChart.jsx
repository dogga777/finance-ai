import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export default function CashFlowChart({ values = [] }) {
  const data = values.map((value, index) => ({
    period: `+${index + 1}`,
    cashflow: value,
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
        <XAxis dataKey="period" />
        <YAxis />
        <Tooltip formatter={(v) => Number(v).toLocaleString()} />
        <Line
          type="monotone"
          dataKey="cashflow"
          stroke="#2563eb"
          strokeWidth={2.5}
          dot={{ r: 5, fill: "#2563eb" }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
