import { Link, useLocation } from "react-router-dom";
import {
  FaHome,
  FaUpload,
  FaRobot,
  FaFileMedical,
  FaCalendarCheck,
  FaUserCircle,
  FaChartBar,
  FaUsers,
  FaCog
} from "react-icons/fa";

import { motion } from "framer-motion";

function Sidebar() {

    const location = useLocation();

    const role = localStorage.getItem("role");

    const menu = [

        {
            title:"Dashboard",
            icon:<FaHome/>,
            path:"/dashboard"
        },

        {
            title:"Upload Report",
            icon:<FaUpload/>,
            path:"/upload"
        },

        {
            title:"AI Chat",
            icon:<FaRobot/>,
            path:"/chatbot"
        },


        {
            title:"Appointment",
            icon:<FaCalendarCheck/>,
            path:"/appointments"
        },

        {
            title:"Profile",
            icon:<FaUserCircle/>,
            path:"/profile"
        }

    ];

    return(

<motion.div

initial={{x:-100}}

animate={{x:0}}

transition={{duration:.5}}

style={styles.sidebar}

>

<h2 style={styles.logo}>

DIAGNOAI

</h2>

{

menu.map((item,index)=>(

<Link

key={index}

to={item.path}

style={

location.pathname===item.path

?

{

...styles.active

}

:

styles.link

}

>

<span style={{fontSize:22}}>

{item.icon}

</span>

<span>

{item.title}

</span>

</Link>

))

}

{

role==="admin" && (

<>

<hr style={{margin:"25px 0"}}/>

<h3 style={styles.adminTitle}>

ADMIN

</h3>

<Link

to="/admin"

style={styles.adminLink}

>

<FaChartBar/>

Dashboard

</Link>

<Link

to="/admin/users"

style={styles.adminLink}

>

<FaUsers/>

Users

</Link>

<Link

to="/admin/settings"

style={styles.adminLink}

>

<FaCog/>

Settings

</Link>

</>

)

}

</motion.div>

    );

}

const styles={

sidebar:{

width:"260px",

height:"100vh",

background:"#fff",

borderRight:"4px solid gold",

padding:"30px",

position:"fixed",

left:0,

top:0,

boxShadow:"5px 0 20px rgba(0,0,0,.08)"

},

logo:{

color:"#d62828",

fontWeight:"900",

fontSize:"30px",

textAlign:"center",

marginBottom:"40px"

},

link:{

display:"flex",

alignItems:"center",

gap:"15px",

padding:"15px",

marginBottom:"15px",

borderRadius:"12px",

textDecoration:"none",

color:"#000",

fontWeight:"600",

transition:".3s"

},

active:{

display:"flex",

alignItems:"center",

gap:"15px",

padding:"15px",

marginBottom:"15px",

borderRadius:"12px",

textDecoration:"none",

background:"#1976d2",

color:"#fff",

fontWeight:"700"

},

adminTitle:{

color:"#d62828",

marginBottom:"15px"

},

adminLink:{

display:"flex",

alignItems:"center",

gap:"12px",

padding:"14px",

marginBottom:"12px",

background:"gold",

borderRadius:"10px",

textDecoration:"none",

color:"#000",

fontWeight:"700"

}

};

export default Sidebar;