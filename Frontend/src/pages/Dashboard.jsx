import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Footer from "../components/Footer";

import {
  FaHeartbeat,
  FaRobot,
  FaUpload,
  FaCalendarCheck,
  FaFileMedical,
  FaChartLine,
} from "react-icons/fa";

import { motion } from "framer-motion";

function Dashboard() {
  const navigate = useNavigate();

  const [stats, setStats] = useState({
    total_users: 0,
    total_reports: 0,
    total_appointments: 0,
  });

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/dashboard");
      setStats(res.data);
    } catch (error) {
      console.log(error);
    }
  };

  const cards = [
    {
      title: "Users",
      value: stats.total_users,
      color: "#d62828",
      icon: <FaHeartbeat size={40} />,
    },
    {
      title: "Reports",
      value: stats.total_reports,
      color: "#1976d2",
      icon: <FaFileMedical size={40} />,
    },
    {
      title: "Appointments",
      value: stats.total_appointments,
      color: "green",
      icon: <FaCalendarCheck size={40} />,
    },
    {
      title: "AI Chat",
      value: "Active",
      color: "orange",
      icon: <FaRobot size={40} />,
    },
  ];

  return (
    <>
      <Navbar />

      <div style={styles.container}>
        <Sidebar />

        <div style={styles.main}>
          <motion.h1
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            style={styles.heading}
          >
            Welcome to <span style={{ color: "#d62828" }}>DIAGNOAI</span>
          </motion.h1>

          {/* Cards */}
          <div style={styles.cardContainer}>
            {cards.map((card, index) => (
              <motion.div
                key={index}
                whileHover={{ scale: 1.05, y: -8 }}
                style={{
                  ...styles.card,
                  borderTop: `6px solid ${card.color}`,
                }}
              >
                <div style={{ color: card.color }}>{card.icon}</div>
                <h2>{card.value}</h2>
                <p>{card.title}</p>
              </motion.div>
            ))}
          </div>

          {/* Quick Actions */}
          <h2 style={styles.sectionTitle}>Quick Actions</h2>

          <div style={styles.actionContainer}>
            <button
              style={styles.blueBtn}
              onClick={() => navigate("/upload")}
            >
              <FaUpload /> Upload Report
            </button>

            <button
              style={styles.redBtn}
              onClick={() => navigate("/chatbot")}
            >
              <FaRobot /> Ask AI
            </button>

            <button
              style={styles.greenBtn}
              onClick={() => navigate("/appointments")}
            >
              <FaCalendarCheck /> Book Appointment
            </button>
          </div>

          {/* Health Summary */}
          <div style={styles.summary}>
            <h2>Health Summary</h2>

            <div style={styles.progress}>
              <div style={styles.progressFill}></div>
            </div>

            <p>
              Upload your blood reports to generate personalized health insights.
            </p>
          </div>

          {/* Analytics */}
          <div style={styles.analytics}>
            <FaChartLine size={45} color="#1976d2" />

            <h2>Health Analytics</h2>

            <p>
              Charts showing haemoglobin, glucose, cholesterol and risk trends
              will appear after report analysis.
            </p>
          </div>
        </div>
      </div>

      <Footer />
    </>
  );
}

const styles = {
  container: {
    display: "flex",
    background: "#f8f9fa",
    minHeight: "100vh",
  },
  main: {
    marginLeft: "280px",
    width: "100%",
    padding: "40px",
  },
  heading: {
    fontSize: "40px",
    marginBottom: "30px",
  },
  cardContainer: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
    gap: "25px",
  },
  card: {
    background: "#fff",
    borderRadius: "18px",
    padding: "30px",
    textAlign: "center",
    border: "2px solid gold",
    boxShadow: "0 8px 25px rgba(0,0,0,.08)",
  },
  sectionTitle: {
    marginTop: "50px",
    color: "#d62828",
  },
  actionContainer: {
    display: "flex",
    gap: "20px",
    flexWrap: "wrap",
    marginTop: "20px",
  },
  blueBtn: {
    background: "#1976d2",
    color: "#fff",
    border: "none",
    padding: "15px 25px",
    borderRadius: "10px",
    cursor: "pointer",
    fontWeight: "bold",
  },
  redBtn: {
    background: "#d62828",
    color: "#fff",
    border: "none",
    padding: "15px 25px",
    borderRadius: "10px",
    cursor: "pointer",
    fontWeight: "bold",
  },
  greenBtn: {
    background: "green",
    color: "#fff",
    border: "none",
    padding: "15px 25px",
    borderRadius: "10px",
    cursor: "pointer",
    fontWeight: "bold",
  },
  summary: {
    marginTop: "40px",
    background: "#fff",
    padding: "30px",
    borderRadius: "18px",
    border: "2px solid gold",
  },
  progress: {
    width: "100%",
    height: "18px",
    background: "#ddd",
    borderRadius: "10px",
    margin: "20px 0",
  },
  progressFill: {
    width: "85%",
    height: "100%",
    background: "#d62828",
    borderRadius: "10px",
  },
  analytics: {
    marginTop: "40px",
    background: "#fff",
    padding: "40px",
    borderRadius: "18px",
    border: "2px solid gold",
    textAlign: "center",
  },
};

export default Dashboard;