import { useEffect, useState } from "react";
import api from "../api/axios";
import { logoutUser } from "../utils/auth";

import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

const DashboardPage = () => {
  const [data, setData] = useState<any>(null);
  const [industry, setIndustry] = useState("");
  const [year, setYear] = useState("");

  const fetchDashboard = async () => {
    const params: any = {};
    if (industry) params.industry = industry;
    if (year) params.year = year;

    const res = await api.get("/dashboard", { params });
    setData(res.data);
  };

  useEffect(() => {
    fetchDashboard();
  }, [industry, year]);

  if (!data) return <p style={{ padding: 20 }}>Loading dashboard...</p>;

  const handleLogout = () => {
    logoutUser();
    window.location.replace("/login");
  };

  const chartData = Object.keys(data.year_breakdown || {}).map((y) => ({
    year: y,
    profit: data.profit_by_year?.[y] || 0,
    revenue: data.revenue_by_year?.[y] || 0,
    expenses: data.expenses_by_year?.[y] || 0,
  }));

  return (
    <div style={{ padding: 32 }}>
      <h2>📊 Analysis Dashboard</h2>

      {/* LOGOUT */}
      <button
        onClick={handleLogout}
        style={{
          position: "absolute",
          top: 20,
          right: 20,
          background: "#e53935",
          color: "#fff",
          border: "none",
          padding: "8px 14px",
          borderRadius: 8,
          cursor: "pointer",
        }}
      >
        Logout
      </button>

      {/* FILTERS */}
      <div style={{ display: "flex", gap: 12, marginBottom: 24 }}>
        <select value={industry} onChange={(e) => setIndustry(e.target.value)}>
          <option value="">All Industries</option>
          <option>Agriculture</option>
          <option>Manufacturing</option>
          <option>Retail</option>
          <option>Logistics</option>
          <option>Ecommerce</option>
        </select>

        <select value={year} onChange={(e) => setYear(e.target.value)}>
          <option value="">All Years</option>
          {Object.keys(data.year_breakdown || {}).map((y) => (
            <option key={y} value={y}>{y}</option>
          ))}
        </select>
      </div>

      {/* KPI */}
      <div style={{ display: "flex", gap: 16 }}>
        <KPI title="Total Analyses" value={data.total_analyses} />
        <KPI title="Avg Score" value={data.average_health_score} />
        <KPI title="Best" value={data.best_health_score} />
        <KPI title="Worst" value={data.worst_health_score} />
      </div>

      {/* PROFIT BAR CHART */}
      <h3 style={{ marginTop: 40 }}>💰 Profit vs Year</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid stroke="#444" strokeDasharray="3 3" />
          <XAxis dataKey="year" label={{ value: "Year", position: "insideBottom", offset: -5 }} />
          <YAxis label={{ value: "Profit (₹)", angle: -90, position: "insideLeft" }} />
          <Tooltip formatter={(v) => `₹ ${Number(v).toLocaleString()}`} />
          <Legend />
          <Bar dataKey="profit" fill="#4CAF50" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>

      {/* REVENUE vs EXPENSE LINE CHART */}
      <h3 style={{ marginTop: 40 }}>📈 Revenue vs Expenses</h3>
      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={chartData}>
          <CartesianGrid stroke="#444" strokeDasharray="3 3" />
          <XAxis dataKey="year" label={{ value: "Year", position: "insideBottom", offset: -5 }} />
          <YAxis label={{ value: "Amount (₹)", angle: -90, position: "insideLeft" }} />
          <Tooltip formatter={(v) => `₹ ${Number(v).toLocaleString()}`} />
          <Legend />
          <Line dataKey="revenue" name="Revenue" stroke="#42A5F5" strokeWidth={3} />
          <Line dataKey="expenses" name="Expenses" stroke="#EF5350" strokeWidth={3} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

const KPI = ({ title, value }: any) => (
  <div style={{ background: "#1e1e1e", padding: 16, borderRadius: 10, minWidth: 140 }}>
    <h4 style={{ opacity: 0.7 }}>{title}</h4>
    <h2>{value}</h2>
  </div>
);

export default DashboardPage;
