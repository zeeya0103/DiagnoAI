import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  FaHeartbeat,
  FaRobot,
  FaSignOutAlt,
  FaUserCircle,
} from "react-icons/fa";

function Navbar() {
  const navigate = useNavigate();

  const role = localStorage.getItem("role");

  const logout = () => {
    localStorage.clear();
    navigate("/");
  };

  return (
    <motion.nav
      initial={{ y: -80 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.6 }}
      style={styles.nav}
    >
      {/* LOGO */}
      <Link to="/" style={styles.logo}>
        <FaHeartbeat color="red" size={30} />
        <span style={styles.logoText}>DIAGNOAI</span>
      </Link>

      {/* LINKS */}
      <div style={styles.links}>
        <Link style={styles.link} to="/">Home</Link>
        <Link style={styles.link} to="/dashboard">Dashboard</Link>
        <Link style={styles.link} to="/upload">Upload Report</Link>
        <Link style={styles.link} to="/chatbot">AI Chat</Link>
        <Link style={styles.link} to="/appointments">Appointment</Link>

        {/* ADMIN */}
        {role === "admin" && (
          <Link style={styles.adminBtn} to="/admin">
            Admin
          </Link>
        )}

        {/* RIGHT ICONS */}
        <FaUserCircle size={28} color="#d62828" style={{ marginLeft: 20 }} />

        <FaRobot size={28} color="#1976d2" style={{ marginLeft: 15 }} />

        <FaSignOutAlt
          onClick={logout}
          size={25}
          color="red"
          style={{
            cursor: "pointer",
            marginLeft: 20,
          }}
        />
      </div>
    </motion.nav>
  );
}

const styles = {
  nav: {
    width: "100%",
    height: "80px",
    background: "#fff",
    borderBottom: "4px solid gold",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "0 50px",
    position: "sticky",
    top: 0,
    zIndex: 999,
    boxShadow: "0 5px 20px rgba(0,0,0,.12)",
  },

  logo: {
    display: "flex",
    alignItems: "center",
    textDecoration: "none",
  },

  logoText: {
    color: "#d62828",
    fontWeight: "900",
    fontSize: "30px",
    marginLeft: "10px",
    letterSpacing: "2px",
  },

  links: {
    display: "flex",
    alignItems: "center",
    gap: "25px",
  },

  link: {
    color: "#000",
    fontWeight: "600",
    textDecoration: "none",
  },

  adminBtn: {
    background: "gold",
    color: "#000",
    padding: "10px 22px",
    borderRadius: "10px",
    fontWeight: "bold",
    textDecoration: "none",
  },
};

export default Navbar;