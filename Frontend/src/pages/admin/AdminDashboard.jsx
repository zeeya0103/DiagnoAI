import Navbar from "../../components/Navbar";
import Sidebar from "../../components/Sidebar";
import Footer from "../../components/Footer";

import { motion } from "framer-motion";

import {
FaUsers,
FaFileMedical,
FaCalendarAlt,
FaChartBar
} from "react-icons/fa";

function AdminDashboard(){

const cards=[

{
title:"Total Users",
value:"324",
icon:<FaUsers size={40}/>,
color:"#1976d2"
},

{
title:"Reports",
value:"1254",
icon:<FaFileMedical size={40}/>,
color:"#d62828"
},

{
title:"Appointments",
value:"86",
icon:<FaCalendarAlt size={40}/>,
color:"green"
},

{
title:"Predictions",
value:"3100",
icon:<FaChartBar size={40}/>,
color:"orange"
}

];

return(

<>

<Navbar/>

<div style={styles.container}>

<Sidebar/>

<div style={styles.main}>

<h1 style={styles.heading}>

Admin Dashboard

</h1>

<div style={styles.grid}>

{

cards.map((item,index)=>(

<motion.div

key={index}

whileHover={{scale:1.05}}

style={{

...styles.card,

borderTop:`6px solid ${item.color}`

}}

>

<div style={{color:item.color}}>

{item.icon}

</div>

<h2>

{item.value}

</h2>

<p>

{item.title}

</p>

</motion.div>

))

}

</div>

<div style={styles.panel}>

<h2>

System Status

</h2>

<ul>

<li>✔ FastAPI Running</li>

<li>✔ MySQL Connected</li>

<li>✔ OpenAI Connected</li>

<li>✔ ML Models Loaded</li>

<li>✔ PDF Parser Active</li>

</ul>

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

main:{
marginLeft:"270px",
padding:"40px",
width:"100%"
},

heading:{
fontSize:"40px",
color:"#d62828"
},

grid:{
display:"grid",
gridTemplateColumns:"repeat(auto-fit,minmax(220px,1fr))",
gap:"25px",
marginTop:"35px"
},

card:{
background:"#fff",
padding:"30px",
borderRadius:"20px",
border:"3px solid gold",
textAlign:"center",
boxShadow:"0 10px 25px rgba(0,0,0,.08)"
},

panel:{
marginTop:"40px",
background:"#fff",
padding:"30px",
borderRadius:"20px",
border:"3px solid gold"
}

};

export default AdminDashboard;