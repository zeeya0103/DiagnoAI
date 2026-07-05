import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Footer from "../components/Footer";
import axios from "axios";
import { motion } from "framer-motion";
import { FaFileMedical, FaDownload } from "react-icons/fa";

function Reports() {

    const [reports,setReports]=useState([]);

    useEffect(()=>{

        loadReports();

    },[]);

    const loadReports=async()=>{

        try{

            const res=await axios.get(

                "http://127.0.0.1:8000/reports",

                {

                    headers:{
                        Authorization:`Bearer ${localStorage.getItem("token")}`
                    }

                }

            );

            setReports(res.data);

        }

        catch{

            console.log("Unable to Load Reports");

        }

    };

return(

<>

<Navbar/>

<div style={styles.container}>

<Sidebar/>

<div style={styles.content}>

<h1 style={styles.heading}>

My Reports

</h1>

<div style={styles.grid}>

{

reports.map((item,index)=>(

<motion.div

key={index}

whileHover={{scale:1.05}}

style={styles.card}

>

<FaFileMedical

size={55}

color="#d62828"

/>

<h2>

{item.file_name}

</h2>

<p>

Disease :

<b>

{item.prediction}

</b>

</p>

<p>

Risk :

<b>

{item.risk}

</b>

</p>

<p>

Date :

{item.created_at}

</p>

<button style={styles.button}>

<FaDownload/>

 Download

</button>

</motion.div>

))

}

</div>

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

heading:{
color:"#d62828",
marginBottom:"35px"
},

grid:{
display:"grid",
gridTemplateColumns:"repeat(auto-fit,minmax(300px,1fr))",
gap:"25px"
},

card:{
background:"#fff",
padding:"25px",
borderRadius:"18px",
border:"3px solid gold",
boxShadow:"0 5px 20px rgba(0,0,0,.08)",
textAlign:"center"
},

button:{
marginTop:"20px",
background:"#1976d2",
color:"#fff",
padding:"12px 25px",
border:"none",
borderRadius:"10px",
cursor:"pointer"
}

};

export default Reports;