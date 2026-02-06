import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchHistory } from "../api/history";

const industries = [
  "Agriculture",
  "Manufacturing",
  "Retail",
  "Logistics",
  "Ecommerce",
];

const HistoryPage = () => {
  const [industry, setIndustry] = useState("Agriculture");
  const [records, setRecords] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    loadHistory();
  }, [industry]);

  const loadHistory = async () => {
    try {
      setLoading(true);
      const data = await fetchHistory(industry);
      setRecords(data.results || []);
    } catch {
      alert("Failed to load history");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "radial-gradient(circle at center, #1f1f1f, #0f0f0f)",
        padding: "40px",
        color: "#fff",
      }}
    >
      <h2 style={{ marginBottom: "20px" }}>📜 Analysis History</h2>

      <select
        value={industry}
        onChange={(e) => setIndustry(e.target.value)}
        style={{
          padding: "10px",
          borderRadius: "8px",
          background: "#121212",
          color: "#fff",
          border: "1px solid #333",
          marginBottom: "20px",
        }}
      >
        {industries.map((i) => (
          <option key={i}>{i}</option>
        ))}
      </select>

      {loading && <p>Loading...</p>}

      {!loading && records.length === 0 && (
        <p>No analyses found for this industry.</p>
      )}

      <div style={{ display: "grid", gap: "14px", marginTop: "20px" }}>
        {records.map((r) => (
          <div
            key={r.id}
            style={{
              background: "#1e1e1e",
              padding: "16px",
              borderRadius: "10px",
              cursor: "pointer",
              border: "1px solid #2a2a2a",
            }}
            onClick={() =>
              navigate(`/result/${industry.toLowerCase()}/${r.id}`)
            }
          >
            <div style={{ fontWeight: 600 }}>
              Year: {r.year ?? "-"} | Health: {r.health_status}
            </div>
            <div style={{ fontSize: "13px", opacity: 0.7 }}>
              Profit: ₹{r.profit} | Score: {r.health_score}
            </div>
            <div style={{ fontSize: "12px", opacity: 0.5 }}>
              {new Date(r.created_at).toLocaleString()}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HistoryPage;
