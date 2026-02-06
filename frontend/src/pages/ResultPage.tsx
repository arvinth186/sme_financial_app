import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../api/axios";

export default function ResultPage() {
  const { industry, id } = useParams<{ industry: string; id: string }>();

  const [analysis, setAnalysis] = useState<any>(null);
  const [ai, setAI] = useState<any>(null);

  useEffect(() => {
    if (!industry || !id) return;

    // 1️⃣ Fetch financial analysis
    api
      .get(`/${industry.toLowerCase()}/analyses/${id}`)
      .then((res) => {
        console.log("ANALYSIS API:", res.data);
        setAnalysis(res.data);
      })
      .catch(console.error);

    // 2️⃣ Fetch AI explanation
    api
      .get(`/${industry.toLowerCase()}/analyses/${id}/ai`)
      .then((res) => {
        console.log("AI API:", res.data);
        setAI(res.data.ai_explanation);
      })
      .catch(console.error);
  }, [industry, id]);

  if (!analysis) return <p>Loading analysis...</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h2>{industry} Financial Summary</h2>

      <p>Total Revenue: ₹{analysis.total_revenue}</p>
      <p>Profit: ₹{analysis.profit}</p>
      <p>Health Score: {analysis.health_score}</p>

      {ai && (
        <>
          <h3>AI Insights</h3>
          <pre>{JSON.stringify(ai, null, 2)}</pre>
        </>
      )}
    </div>
  );
}
