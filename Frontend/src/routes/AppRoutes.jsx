import { Routes, Route, Navigate } from "react-router-dom";

import Home from "../pages/Home";
import Dashboard from "../pages/Dashboard";
import UploadReport from "../pages/UploadReport";
import Reports from "../pages/Reports";
import Chatbot from "../pages/Chatbot";
import Appointments from "../pages/Appointments";
import Profile from "../pages/Profile";

import AdminDashboard from "../pages/admin/AdminDashboard";
import Users from "../pages/admin/Users";
import Analytics from "../pages/admin/Analytics";
import Settings from "../pages/admin/Settings";

import AdminRoute from "../components/AdminRoute";

function AppRoutes() {
  return (
    <Routes>
      {/* PUBLIC */}
      <Route path="/" element={<Home />} />

      {/* USER ROUTES */}
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/upload" element={<UploadReport />} />
      <Route path="/reports" element={<Reports />} />
      <Route path="/chatbot" element={<Chatbot />} />
      <Route path="/appointments" element={<Appointments />} />
      <Route path="/profile" element={<Profile />} />

      {/* ADMIN */}
      <Route
        path="/admin"
        element={
          <AdminRoute>
            <AdminDashboard />
          </AdminRoute>
        }
      />

      <Route
        path="/admin/users"
        element={
          <AdminRoute>
            <Users />
          </AdminRoute>
        }
      />

      <Route
        path="/admin/analytics"
        element={
          <AdminRoute>
            <Analytics />
          </AdminRoute>
        }
      />

      <Route
        path="/admin/settings"
        element={
          <AdminRoute>
            <Settings />
          </AdminRoute>
        }
      />

      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}

export default AppRoutes;