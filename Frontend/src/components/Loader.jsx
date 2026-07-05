import { motion } from "framer-motion";
import { FaHeartbeat, FaRobot } from "react-icons/fa";

function Loader() {
  return (
    <div style={styles.container}>
      <motion.div
        animate={{
          scale: [1, 1.2, 1],
          rotate: [0, 360],
        }}
        transition={{
          repeat: Infinity,
          duration: 2,
        }}
        style={styles.outerCircle}
      >
        <motion.div
          animate={{
            scale: [1, 0.9, 1],
          }}
          transition={{
            repeat: Infinity,
            duration: 1,
          }}
          style={styles.innerCircle}
        >
          <FaHeartbeat size={70} color="#d62828" />
        </motion.div>
      </motion.div>

      <motion.h1
        animate={{
          opacity: [0.5, 1, 0.5],
        }}
        transition={{
          repeat: Infinity,
          duration: 1.5,
        }}
        style={styles.title}
      >
        DIAGNOAI
      </motion.h1>

      <motion.div
        animate={{
          y: [-10, 10, -10],
        }}
        transition={{
          repeat: Infinity,
          duration: 2,
        }}
      >
        <FaRobot
          size={45}
          color="#1976d2"
        />
      </motion.div>

      <p style={styles.text}>
        Initializing AI Diagnostic Engine...
      </p>
    </div>
  );
}

const styles = {

container:{
display:"flex",
flexDirection:"column",
justifyContent:"center",
alignItems:"center",
height:"100vh",
background:"#fff"
},

outerCircle:{
width:"180px",
height:"180px",
borderRadius:"50%",
border:"8px solid gold",
display:"flex",
justifyContent:"center",
alignItems:"center",
boxShadow:"0 0 40px rgba(255,215,0,.5)"
},

innerCircle:{
width:"120px",
height:"120px",
background:"#fff8dc",
borderRadius:"50%",
display:"flex",
justifyContent:"center",
alignItems:"center"
},

title:{
marginTop:"30px",
fontSize:"40px",
color:"#d62828",
fontWeight:"900",
letterSpacing:"3px"
},

text:{
marginTop:"20px",
fontSize:"18px",
color:"#444"
}

};

export default Loader;