import { Outlet, Navigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Footer from "../components/Footer";

function AdminLayout() {

  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (role !== "admin") {
    return <Navigate to="/" replace />;
  }

  return (
    <>
      <Navbar />

      <div
        style={{
          display: "flex",
          minHeight: "100vh",
          background: "#f5f5f5",
        }}
      >
        <Sidebar />

        <main
          style={{
            flex: 1,
            marginLeft: "270px",
            padding: "35px",
          }}
        >
          <Outlet />
        </main>
      </div>

      <Footer />
    </>
  );
}

export default AdminLayout;