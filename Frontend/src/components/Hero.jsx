import { motion } from "framer-motion";
import { FaRobot, FaHeartbeat, FaFileMedical, FaUserMd } from "react-icons/fa";
import { Link } from "react-router-dom";

function Hero() {
  return (
    <section style={styles.hero}>

      <motion.div
        initial={{ x: -150, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 1 }}
        style={styles.left}
      >
        <h1 style={styles.title}>
          Smart Healthcare with <br />

          <span style={styles.red}>DIAGNOCARE-AI</span>
        </h1>

        <p style={styles.desc}>
          Upload your blood report and let AI analyse your
          health in seconds. Get intelligent insights,
          disease prediction and personalized recommendations.
        </p>

        <div style={styles.buttons}>
          <Link to="/upload">
            <button style={styles.primary}>
              Upload Report
            </button>
          </Link>

          <Link to="/chatbot">
            <button style={styles.secondary}>
              Ask AI
            </button>
          </Link>
        </div>

        <div style={styles.stats}>

          <div style={styles.card}>
            <FaHeartbeat color="red" size={35}/>
            <h2>500+</h2>
            <p>Patients</p>
          </div>

          <div style={styles.card}>
            <FaRobot color="#1976d2" size={35}/>
            <h2>98%</h2>
            <p>AI Accuracy</p>
          </div>

          <div style={styles.card}>
            <FaFileMedical color="green" size={35}/>
            <h2>1500+</h2>
            <p>Reports</p>
          </div>

        </div>

      </motion.div>

      <motion.div
        initial={{ x: 150, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 1 }}
        style={styles.right}
      >

        <motion.div
          animate={{ y: [-15,15,-15] }}
          transition={{
            repeat: Infinity,
            duration: 4
          }}
          style={styles.circle}
        >

          <FaUserMd
            size={180}
            color="#d62828"
          />

        </motion.div>

      </motion.div>

    </section>
  );
}

const styles = {

hero:{
display:"flex",
justifyContent:"space-between",
alignItems:"center",
padding:"80px",
minHeight:"90vh",
background:"#fff"
},

left:{
width:"55%"
},

right:{
width:"40%",
display:"flex",
justifyContent:"center"
},

title:{
fontSize:"60px",
fontWeight:"900",
color:"#000",
lineHeight:"75px"
},

red:{
color:"#d62828"
},

desc:{
marginTop:"30px",
fontSize:"20px",
lineHeight:"34px",
color:"#444"
},

buttons:{
display:"flex",
gap:"20px",
marginTop:"40px"
},

primary:{
background:"#1976d2",
color:"#fff",
padding:"15px 35px",
border:"none",
borderRadius:"12px",
fontSize:"18px",
fontWeight:"700"
},

secondary:{
background:"#d62828",
color:"#fff",
padding:"15px 35px",
border:"none",
borderRadius:"12px",
fontSize:"18px",
fontWeight:"700"
},

stats:{
display:"flex",
gap:"25px",
marginTop:"60px"
},

card:{
border:"3px solid gold",
padding:"20px",
borderRadius:"20px",
width:"180px",
textAlign:"center",
boxShadow:"0 8px 25px rgba(0,0,0,.08)"
},

circle:{
width:"350px",
height:"350px",
background:"#fff8dc",
borderRadius:"50%",
display:"flex",
justifyContent:"center",
alignItems:"center",
border:"6px solid gold",
boxShadow:"0 15px 40px rgba(0,0,0,.15)"
}

};

export default Hero;