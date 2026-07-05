import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import Footer from "../components/Footer";

import { motion } from "framer-motion";
import {
  FaHeartbeat,
  FaRobot,
  FaMicroscope,
  FaUserMd,
  FaUpload,
  FaChartLine,
} from "react-icons/fa";

function Home() {
  const features = [
    {
      icon: <FaHeartbeat size={40} color="#d62828" />,
      title: "Disease Prediction",
      text: "Predict anemia, diabetes and other diseases using AI-powered models.",
    },
    {
      icon: <FaRobot size={40} color="#1976d2" />,
      title: "AI Chatbot",
      text: "Ask health-related questions and receive intelligent responses instantly.",
    },
    {
      icon: <FaMicroscope size={40} color="green" />,
      title: "Blood Report Analysis",
      text: "Upload pathology reports and receive simplified health insights.",
    },
    {
      icon: <FaUserMd size={40} color="#d62828" />,
      title: "Doctor Friendly",
      text: "Designed for patients and diagnostic laboratories.",
    },
    {
      icon: <FaUpload size={40} color="#1976d2" />,
      title: "Easy Upload",
      text: "Drag & Drop PDF reports for automatic analysis.",
    },
    {
      icon: <FaChartLine size={40} color="orange" />,
      title: "Health Analytics",
      text: "Interactive graphs to monitor your health over time.",
    },
  ];

  return (
    <>
      <Navbar />

      <Hero />

      {/* Features */}
      <section style={styles.section}>
        <h1 style={styles.heading}>
          Why Choose <span style={{ color: "#d62828" }}>DIAGNOCARE-AI</span>?
        </h1>

        <div style={styles.grid}>
          {features.map((item, index) => (
            <motion.div
              key={index}
              whileHover={{
                scale: 1.05,
                y: -10,
              }}
              style={styles.card}
            >
              {item.icon}

              <h2 style={styles.cardTitle}>{item.title}</h2>

              <p style={styles.cardText}>{item.text}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Statistics */}
      <section style={styles.statsSection}>
        <motion.div whileHover={{ scale: 1.1 }} style={styles.statCard}>
          <h1>500+</h1>
          <p>Patients</p>
        </motion.div>

        <motion.div whileHover={{ scale: 1.1 }} style={styles.statCard}>
          <h1>98%</h1>
          <p>Prediction Accuracy</p>
        </motion.div>

        <motion.div whileHover={{ scale: 1.1 }} style={styles.statCard}>
          <h1>1500+</h1>
          <p>Reports Analysed</p>
        </motion.div>

        <motion.div whileHover={{ scale: 1.1 }} style={styles.statCard}>
          <h1>24×7</h1>
          <p>AI Assistant</p>
        </motion.div>
      </section>

      {/* CTA */}
      <section style={styles.cta}>
        <motion.h1
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 1 }}
        >
          Smart Healthcare Begins Here
        </motion.h1>

        <p>
          Upload your blood report and receive AI-generated insights within
          seconds.
        </p>

        <button style={styles.button}>Start Diagnosis</button>
      </section>

      <Footer />
    </>
  );
}

const styles = {
  section: {
    padding: "80px",
    background: "#fff",
  },

  heading: {
    textAlign: "center",
    fontSize: "45px",
    marginBottom: "50px",
    color: "#000",
  },

  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit,minmax(300px,1fr))",
    gap: "30px",
  },

  card: {
    border: "3px solid gold",
    borderRadius: "20px",
    padding: "30px",
    textAlign: "center",
    boxShadow: "0 8px 25px rgba(0,0,0,.1)",
    background: "#fff",
  },

  cardTitle: {
    marginTop: "20px",
    color: "#d62828",
    fontSize: "24px",
  },

  cardText: {
    marginTop: "15px",
    color: "#444",
    lineHeight: "28px",
  },

  statsSection: {
    background: "#1976d2",
    color: "#fff",
    display: "flex",
    justifyContent: "space-evenly",
    flexWrap: "wrap",
    padding: "70px 20px",
  },

  statCard: {
    textAlign: "center",
    border: "3px solid gold",
    borderRadius: "15px",
    padding: "30px",
    width: "220px",
    margin: "15px",
    background: "#1565c0",
  },

  cta: {
    textAlign: "center",
    padding: "90px 20px",
    background: "#fff8dc",
  },

  button: {
    marginTop: "30px",
    background: "#d62828",
    color: "#fff",
    border: "none",
    padding: "15px 35px",
    borderRadius: "10px",
    fontSize: "18px",
    fontWeight: "bold",
    cursor: "pointer",
  },
};

export default Home;