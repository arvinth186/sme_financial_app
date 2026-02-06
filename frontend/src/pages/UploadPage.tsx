import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { uploadFinancialCSV } from "../api/upload";
import { logoutUser } from "../utils/auth";
import api from "../api/axios";


const UploadPage = () => {
  const [industry, setIndustry] = useState("Agriculture");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState("en");


  const navigate = useNavigate();

  const handleLogout = () => {
    logoutUser();
    navigate("/login", { replace: true });
  };


  const handleUpload = async () => {
    if (!file) {
      alert("Please select a CSV file");
      return;
    }

    try {
      setLoading(true);
      const result = await uploadFinancialCSV(industry, file, language);
      navigate(`/result/${industry.toLowerCase()}/${result.record_id}`);
    } catch (err) {
      console.error(err);
      alert("Upload failed. Check backend.");
    } finally {
      setLoading(false);
    }
  };

  

const downloadTemplate = async () => {
  if (!industry) return alert("Select industry first");

  const industryKey = industry.toLowerCase();

  const response = await api.get(`/templates/${industryKey}`, {
    responseType: "blob",
  });

  const blob = new Blob([response.data], { type: "text/csv" });
  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = `${industryKey}_template.csv`;
  document.body.appendChild(a);
  a.click();
  a.remove();

  window.URL.revokeObjectURL(url);
};


  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100%",
        background: "radial-gradient(circle at center, #1f1f1f, #0f0f0f)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "24px",
        boxSizing: "border-box",
      }}
    > 
    <button
  onClick={handleLogout}
  style={{
    position: "absolute",
    top: "20px",
    left: "20px",
    background: "#e53935",
    color: "#fff",
    border: "none",
    padding: "8px 14px",
    borderRadius: "8px",
    fontSize: "14px",
    fontWeight: 600,
    cursor: "pointer",
  }}
>
  Logout
</button>

<button
  onClick={() => navigate("/history")}
  style={{
    position: "absolute",
    top: "20px",
    right: "20px",
    background: "#2196F3",
    color: "#fff",
    border: "none",
    padding: "8px 14px",
    borderRadius: "8px",
    fontSize: "14px",
    fontWeight: 600,
    cursor: "pointer",
  }}
>
  History
</button>


<button
  onClick={() => navigate("/dashboard")}
  style={{
    position: "absolute",
    top: "20px",
    right: "140px",
    background: "#4CAF50",
    color: "#fff",
    border: "none",
    padding: "8px 14px",
    borderRadius: "8px",
    fontSize: "14px",
    fontWeight: 600,
    cursor: "pointer",
  }}
>
  Dashboard
</button>

{/* TEMPLATE DOWNLOAD */}
<button
  onClick={downloadTemplate}
  style={{
    position: "absolute",
    top: "20px",
    right: "260px",
    padding: "10px",
    background: "#2e7d32",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    fontWeight: 600,
    cursor: "pointer",
  }}
>
  📥 Download {industry} CSV Template
</button>

      <div
        style={{
          background: "#1e1e1e",
          borderRadius: "14px",
          padding: "32px",
          width: "100%",
          maxWidth: "420px",
          boxShadow: "0 12px 40px rgba(0,0,0,0.6)",
        }}
      >
        {/* TITLE */}
        <h2 style={{ marginBottom: "8px" }}>
          SME Financial Health Platform
        </h2>
        <p style={{ opacity: 0.7, marginBottom: "24px" }}>
          Upload your financial CSV or Excel file to generate insights & reports
        </p>

        {/* INDUSTRY SELECT */}
        <label style={labelStyle}>Select Industry</label>
        <select
          value={industry}
          onChange={(e) => setIndustry(e.target.value)}
          style={inputStyle}
        >
          <option>Agriculture</option>
          <option>Manufacturing</option>
          <option>Retail</option>
          <option>Logistics</option>
          <option>Ecommerce</option>
        </select>

        <label>Select Language</label>
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          style={inputStyle}
        >
          <option value="en">English</option>
          <option value="ta">தமிழ்</option>
          <option value="hi">हिन्दी</option>
        </select>


        {/* FILE INPUT */}
        <label style={{ ...labelStyle, marginTop: "16px" }}>
          Upload CSV or Excel File
        </label>

        <div
          style={{
            background: "#121212",
            border: "1px dashed #444",
            borderRadius: "8px",
            padding: "12px",
            textAlign: "center",
            cursor: "pointer",
          }}
        >
          <input
            type="file"
            accept=".csv,.xlsx"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            style={{ width: "100%" }}
          />
          {file && (
            <p style={{ marginTop: "8px", fontSize: "13px", opacity: 0.8 }}>
              📄 {file.name}
            </p>
          )}
        </div>

        {/* BUTTON */}
        <button
          onClick={handleUpload}
          disabled={loading}
          style={{
            width: "100%",
            marginTop: "24px",
            padding: "12px",
            background: loading ? "#555" : "#2196F3",
            color: "#fff",
            border: "none",
            borderRadius: "8px",
            fontSize: "15px",
            fontWeight: 600,
            cursor: loading ? "not-allowed" : "pointer",
            transition: "0.2s",
          }}
        >
          {loading ? "Uploading..." : "🚀 Upload & Analyze"}
        </button>
      </div>
    </div>
  );
};

export default UploadPage;

/* ===== SHARED STYLES ===== */

const labelStyle: React.CSSProperties = {
  display: "block",
  marginBottom: "6px",
  fontSize: "14px",
  opacity: 0.8,
};

const inputStyle: React.CSSProperties = {
  width: "100%",
  padding: "10px",
  borderRadius: "8px",
  border: "1px solid #333",
  background: "#121212",
  color: "#fff",
};

