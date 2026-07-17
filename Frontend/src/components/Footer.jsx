import { motion } from "framer-motion";
import {
  FaHeartbeat,
  FaGithub,
  FaLinkedin,
  FaEnvelope,
} from "react-icons/fa";

import Signature from "./Signature";

function Footer() {
  return (
    <footer style={styles.footer}>
      <motion.div
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >
        <div style={styles.logo}>
          <FaHeartbeat color="gold" size={35} />
          <h1 style={styles.heading}>DIAGNOCARE-AI</h1>
        </div>

        <p style={styles.text}>
          AI Powered Smart Diagnostic Assistant
        </p>

        <div style={styles.icons}>
          <FaGithub style={styles.icon} />
          <FaLinkedin style={styles.icon} />
          <FaEnvelope style={styles.icon} />
        </div>

        <Signature />

        <hr style={styles.hr} />

        <p style={styles.copy}>
          © 2026 DIAGNOCARE-AI • All Rights Reserved
        </p>
      </motion.div>
    </footer>
  );
}

const styles = {
  footer: {
    background: "#d62828",
    color: "#fff",
    marginTop: "80px",
    padding: "60px 20px",
    borderTop: "6px solid gold",
    textAlign: "center",
  },

  logo: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    gap: "12px",
  },

  heading: {
    color: "#fff",
    fontSize: "38px",
    fontWeight: "900",
    letterSpacing: "2px",
  },

  text: {
    marginTop: "20px",
    fontSize: "18px",
  },

  icons: {
    marginTop: "30px",
    display: "flex",
    justifyContent: "center",
    gap: "30px",
  },

  icon: {
    fontSize: "30px",
    cursor: "pointer",
    transition: ".3s",
  },

  hr: {
    margin: "40px auto",
    width: "70%",
    borderColor: "gold",
  },

  copy: {
    fontSize: "15px",
    color: "#fff8dc",
  },
};

export default Footer;