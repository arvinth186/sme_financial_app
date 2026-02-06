import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../api/axios";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

export default function AgricultureResultPage() {
  const { id } = useParams<{ id: string }>();

  const [analysis, setAnalysis] = useState<any>(null);
  const [ai, setAI] = useState<any>(null);

  useEffect(() => {
    if (!id) return;

    api.get(`/agriculture/analyses/${id}`).then((res) => {
      setAnalysis(res.data);
    });

    api.get(`/agriculture/analyses/${id}/ai`).then((res) => {
      setAI(res.data.ai_explanation);
    });
  }, [id]);

  /* ================= PDF DOWNLOAD ================= */

  const downloadPDF = () => {
  if (!analysis || !ai) return;

  const doc = new jsPDF("p", "mm", "a4");
  const pageHeight = doc.internal.pageSize.height;
  const marginX = 14;
  const contentWidth = 180;
  let y = 14;

  const addPageIfNeeded = (space = 8) => {
    if (y + space > pageHeight - 12) {
      doc.addPage();
      y = 14;
    }
  };

  const writeText = (text: string, indent = 0, size = 11) => {
    doc.setFontSize(size);
    const safeText = text.replace(/₹/g, "Rs.");
    const lines = doc.splitTextToSize(safeText, contentWidth - indent);
    addPageIfNeeded(lines.length * 6);
    doc.text(lines, marginX + indent, y);
    y += lines.length * 6;
  };

  /* ================= HEADER ================= */

  doc.setFontSize(18);
  doc.text("SME Financial Health Report", 105, y, { align: "center" });
  y += 10;

  writeText("Industry: Agriculture", 0, 12);
  writeText(`Report ID: ${id}`, 0, 12);
  writeText(`Generated On: ${new Date().toLocaleString()}`, 0, 12);
  y += 6;

  /* ================= FINANCIAL TABLE ================= */

  autoTable(doc, {
    startY: y,
    head: [["Metric", "Value"]],
    body: [
      ["Total Revenue", `Rs. ${analysis.financials.total_revenue}`],
      ["Total Expenses", `Rs. ${analysis.financials.total_expenses}`],
      ["Profit", `Rs. ${analysis.financials.profit}`],
      ["Profit Margin", `${analysis.financials.profit_margin}%`],
      ["Health Score", analysis.health.health_score],
      ["Credit Risk", analysis.health.credit_risk],
    ],
    styles: { fontSize: 11 },
    headStyles: { fillColor: [33, 150, 243] },
  });

  y = (doc as any).lastAutoTable.finalY + 10;

  /* ================= AI INSIGHTS ================= */

  writeText("AI Insights", 0, 14);
  y += 2;

  writeText("What is going well:", 0, 12);
  ai.Good.forEach((g: string) => writeText(`• ${g}`, 4));

  y += 4;
  writeText("Risks:", 0, 12);
  ai.Risks.forEach((r: string) => writeText(`• ${r}`, 4));

  y += 4;
  writeText("Improvements:", 0, 12);
  ai.Improvement.forEach((i: any) => {
    writeText(`• ${i.action}`, 4);
    writeText(`Benefit: ${i.benefit}`, 8);
    writeText(`Timeline: ${i.timeline}`, 8);
    y += 2;
  });

  y += 4;
  writeText("Guidance:", 0, 12);
  writeText(ai.Guidance, 4);

  /* ================= PRODUCT RECOMMENDATIONS ================= */

  if (ai.ProductRecommendations) {
    y += 6;
    writeText("Product Recommendations", 0, 14);

    Object.entries(ai.ProductRecommendations).forEach(
      ([category, items]: any) => {
        y += 2;
        writeText(`${category}:`, 0, 12);

        items.forEach((p: any) => {
          writeText(`• ${p.product}`, 4);
          writeText(`Reason: ${p.reason}`, 8);
        });
      }
    );
  }

  /* ================= SAVE ================= */

  doc.save(`Agriculture_Report_${id}.pdf`);
};


  /* ================= UI ================= */

  if (!analysis) return <p>Loading Agriculture analysis...</p>;

  const { financials, health } = analysis;

  return (
    <div style={{ padding: "24px" }}>
      {/* HEADER */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "16px",
        }}
      >
        <h2>Agriculture Financial Summary</h2>

        <button
          onClick={downloadPDF}
          style={{
            padding: "10px 16px",
            background: "#2196F3",
            color: "#fff",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
            fontWeight: 600,
          }}
        >
          📄 Download PDF Report
        </button>
      </div>

      {/* METRICS */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
          gap: "16px",
        }}
      >
        <Metric label="Total Revenue" value={`₹${financials.total_revenue}`} />
        <Metric label="Total Expenses" value={`₹${financials.total_expenses}`} />
        <Metric label="Profit" value={`₹${financials.profit}`} />
        <Metric label="Profit Margin" value={`${financials.profit_margin}%`} />
        <Metric label="Health Score" value={health.health_score} />
        <Metric label="Credit Risk" value={health.credit_risk} />
      </div>

      {/* AI INSIGHTS */}
      {ai && (
        <>
          <Section title="What is going well">
            {ai.Good.map((g: string, i: number) => (
              <li key={i}>{g}</li>
            ))}
          </Section>

          <Section title="Risks">
            {ai.Risks.map((r: string, i: number) => (
              <li key={i}>{r}</li>
            ))}
          </Section>

          <Section title="Improvements">
            {ai.Improvement.map((item: any, i: number) => (
              <li key={i}>
                <b>{item.action}</b>
                <br />
                Benefit: {item.benefit}
                <br />
                Timeline: {item.timeline}
              </li>
            ))}
          </Section>

          <Section title="Guidance">
            <p>{ai.Guidance}</p>
          </Section>

          <Section title="Product Recommendations">
            <h4>System Recommended</h4>
            <ul>
              {ai.ProductRecommendations?.System?.map(
                (item: any, i: number) => (
                  <li key={i}>
                    <b>{item.product}</b>
                    <br />
                    {item.reason}
                  </li>
                )
              )}
            </ul>

            {ai.ProductRecommendations?.Additional?.length > 0 && (
              <>
                <h4 style={{ marginTop: "12px" }}>Additional Suggestions</h4>
                <ul>
                  {ai.ProductRecommendations.Additional.map(
                    (item: any, i: number) => (
                      <li key={i}>
                        <b>{item.product}</b>
                        <br />
                        {item.reason}
                      </li>
                    )
                  )}
                </ul>
              </>
            )}
          </Section>
        </>
      )}
    </div>
  );
}

/* ================= SMALL COMPONENTS ================= */

const Metric = ({ label, value }: { label: string; value: any }) => (
  <div
    style={{
      background: "#1e1e1e",
      padding: "16px",
      borderRadius: "8px",
    }}
  >
    <p style={{ opacity: 0.7 }}>{label}</p>
    <h3>{value}</h3>
  </div>
);

const Section = ({ title, children }: any) => (
  <div style={{ marginTop: "24px" }}>
    <h3>{title}</h3>
    <ul>{children}</ul>
  </div>
);
