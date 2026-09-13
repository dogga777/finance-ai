import { Navigate, Route, Routes } from "react-router-dom";

import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import Analysis from "./pages/Analysis";
import Anomalies from "./pages/Anomalies";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Predictions from "./pages/Predictions";
import Register from "./pages/Register";
import Reports from "./pages/Reports";
import Upload from "./pages/Upload";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="upload" element={<Upload />} />
        <Route path="analysis" element={<Analysis />} />
        <Route path="predictions" element={<Predictions />} />
        <Route path="anomalies" element={<Anomalies />} />
        <Route path="reports" element={<Reports />} />
      </Route>

      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
