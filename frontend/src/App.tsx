import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import UploadPage from "./pages/UploadPage";
import ManufacturingResultPage from "./pages/ManufacturingResultPage";
import RetailResultPage from "./pages/RetailResultPage";
import LogisticsResultPage from "./pages/LogisticsResultPage";
import EcommerceResultPage from "./pages/EcommerceResultPage";
import AgricultureResultPage from "./pages/AgricultureResultPage";

import ProtectedRoute from "./components/ProtectedRoute";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import { isAuthenticated } from "./utils/auth";

import HistoryPage from "./pages/HistoryPage";
import DashboardPage from "./pages/DashboardPage";


function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ================= PUBLIC ROUTES ================= */}
        <Route
          path="/login"
          element={
            isAuthenticated() ? <Navigate to="/" replace /> : <LoginPage />
          }
        />

        <Route
          path="/register"
          element={
            isAuthenticated() ? <Navigate to="/" replace /> : <RegisterPage />
          }
        />

        {/* ================= PROTECTED ROUTES ================= */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <UploadPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/result/agriculture/:id"
          element={
            <ProtectedRoute>
              <AgricultureResultPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/result/manufacturing/:id"
          element={
            <ProtectedRoute>
              <ManufacturingResultPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/result/retail/:id"
          element={
            <ProtectedRoute>
              <RetailResultPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/result/logistics/:id"
          element={
            <ProtectedRoute>
              <LogisticsResultPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/result/ecommerce/:id"
          element={
            <ProtectedRoute>
              <EcommerceResultPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/history"
          element={
            <ProtectedRoute>
              <HistoryPage />
            </ProtectedRoute>
          }
        />

        {/* ================= FALLBACK ================= */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
