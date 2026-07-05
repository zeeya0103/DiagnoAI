import Navbar from "../../components/Navbar";
import Sidebar from "../../components/Sidebar";
import Footer from "../../components/Footer";

import {

BarChart,
Bar,
CartesianGrid,
XAxis,
YAxis,
Tooltip,
ResponsiveContainer

} from "recharts";

const data=[

{name:"Anaemia",patients:45},

{name:"Diabetes",patients:62},

{name:"Normal",patients:118},

{name:"High Cholesterol",patients:21}

];

function Analytics(){

return(

<>

<Navbar/>

<div style={{display:"flex"}}>

<Sidebar/>

<div style={{marginLeft:"270px",padding:"50px",width:"100%"}}>

<h1 style={{color:"#d62828"}}>

Analytics

</h1>

<div style={{

height:"450px",

background:"#fff",

padding:"30px",

border:"3px solid gold",

borderRadius:"20px"

}}>

<ResponsiveContainer>

<BarChart data={data}>

<CartesianGrid/>

<XAxis dataKey="name"/>

<YAxis/>

<Tooltip/>

<Bar dataKey="patients"/>

</BarChart>

</ResponsiveContainer>

</div>

</div>

</div>

<Footer/>

</>

);

}

export default Analytics;