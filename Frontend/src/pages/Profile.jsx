import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Footer from "../components/Footer";
import { motion } from "framer-motion";
import { FaUserCircle } from "react-icons/fa";
import { useEffect, useState } from "react";
import axios from "axios";

function Profile() {

const [reports, setReports] = useState(0);
const [appointments, setAppointments] = useState(0);

const user = {

name: localStorage.getItem("name") || "Patient",

email: localStorage.getItem("email") || "patient@email.com",

role: localStorage.getItem("role") || "patient"

};

useEffect(() => {
    fetchReports();
    fetchAppointments();
}, []);

const fetchReports = async () => {
    try {
        const res = await axios.get("http://127.0.0.1:8000/reports/");
        setReports(res.data.length);
    } catch (err) {
        console.log(err);
    }
};

const fetchAppointments = async () => {
    try {
        const res = await axios.get("http://127.0.0.1:8000/appointments/");
        setAppointments(res.data.length);
    } catch (err) {
        console.log(err);
    }
};


return(

<>

<Navbar/>

<div style={styles.container}>

<Sidebar/>

<div style={styles.content}>

<motion.div

initial={{opacity:0}}

animate={{opacity:1}}

style={styles.card}

>

<FaUserCircle

size={120}

color="#1976d2"

/>

<h1>

{user.name}

</h1>

<p>

Email : {user.email}

</p>

<p>

Role : {user.role}

</p>

<div style={styles.info}>

<div style={styles.box}>

<h2>{reports}</h2>

<p>Reports</p>

</div>

<div style={styles.box}>

<h2>{appointments}</h2>

<p>Appointments</p>

</div>

<div style={styles.box}>

<h2>92%</h2>

<p> Rating Score</p>

</div>

</div>

</motion.div>

</div>

</div>

<Footer/>

</>

);

}

const styles={

container:{
display:"flex",
background:"#f5f5f5"
},

content:{
marginLeft:"270px",
width:"100%",
padding:"50px"
},

card:{
background:"#fff",
padding:"40px",
borderRadius:"20px",
border:"3px solid gold",
maxWidth:"700px",
margin:"auto",
textAlign:"center",
boxShadow:"0 10px 30px rgba(0,0,0,.08)"
},

info:{
display:"flex",
justifyContent:"space-around",
marginTop:"40px",
flexWrap:"wrap"
},

box:{
background:"#1976d2",
color:"#fff",
padding:"25px",
width:"160px",
borderRadius:"15px",
margin:"10px"
}

};

export default Profile;