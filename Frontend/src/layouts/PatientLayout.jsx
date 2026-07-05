import { Outlet } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Footer from "../components/Footer";
import { Navigate } from "react-router-dom";

function PatientLayout() {

  const token = localStorage.getItem("token");

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return (
    <>
      <Navbar />

      <div
        style={{
          display: "flex",
          minHeight: "100vh",
          background: "#f8f9fa",
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

export default PatientLayout;