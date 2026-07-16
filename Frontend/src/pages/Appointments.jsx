import { useState } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Footer from "../components/Footer";
import axios from "axios";
import toast from "react-hot-toast";
import { motion } from "framer-motion";

function Appointments() {

  const [form, setForm] = useState({
    patient_name: "",
    email: "",
    phone: "",
    address: "",   // ✅ NEW
    date: "",
    time: ""
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const bookAppointment = async (e) => {
    e.preventDefault();

    try {

      await axios.post(
        "https://diagnoai-1-xywq.onrender.com/appointments",
        form,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`
          }
        }
      );

      toast.success("Appointment Booked Successfully");

      setForm({
        patient_name: "",
        email: "",
        phone: "",
        address: "",   // ✅ RESET
        date: "",
        time: ""
      });

    } catch (error) {
      console.log(error.response?.data || error.message);
      toast.error("Booking Failed");
    }
  };

  return (
    <>
      <Navbar />

      <div style={styles.container}>
        <Sidebar />

        <div style={styles.content}>
          <motion.form
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            style={styles.card}
            onSubmit={bookAppointment}
          >

            <h1 style={styles.heading}>
              Book Appointment
            </h1>

            <input
              style={styles.input}
              placeholder="Patient Name"
              name="patient_name"
              value={form.patient_name}
              onChange={handleChange}
            />

            <input
              style={styles.input}
              placeholder="Email"
              name="email"
              value={form.email}
              onChange={handleChange}
              type="email"
            />

            <input
              style={styles.input}
              placeholder="Phone Number"
              name="phone"
              value={form.phone}
              onChange={handleChange}
            />

            {/* ✅ ADDRESS FIELD */}
            <input
              style={styles.input}
              placeholder="Full Address"
              name="address"
              value={form.address}
              onChange={handleChange}
            />

            <input
              type="date"
              style={styles.input}
              name="date"
              value={form.date}
              onChange={handleChange}
            />

            <input
              type="time"
              style={styles.input}
              name="time"
              value={form.time}
              onChange={handleChange}
            />

            <button style={styles.button}>
              Book Appointment
            </button>

          </motion.form>
        </div>
      </div>

      <Footer />
    </>
  );
}

const styles = {
  container: {
    display: "flex",
    background: "#f5f5f5"
  },
  content: {
    marginLeft: "270px",
    width: "100%",
    padding: "50px"
  },
  card: {
    maxWidth: "550px",
    margin: "auto",
    background: "#fff",
    padding: "40px",
    borderRadius: "20px",
    border: "3px solid gold",
    boxShadow: "0 10px 30px rgba(0,0,0,.08)"
  },
  heading: {
    textAlign: "center",
    marginBottom: "30px",
    color: "#d62828"
  },
  input: {
    width: "100%",
    padding: "15px",
    marginBottom: "20px",
    borderRadius: "10px",
    border: "2px solid gold",
    fontSize: "16px"
  },
  button: {
    width: "100%",
    padding: "15px",
    background: "#1976d2",
    color: "#fff",
    border: "none",
    borderRadius: "10px",
    fontWeight: "bold",
    fontSize: "18px",
    cursor: "pointer"
  }
};

export default Appointments;