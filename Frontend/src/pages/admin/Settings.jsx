import Navbar from "../../components/Navbar";
import Sidebar from "../../components/Sidebar";
import Footer from "../../components/Footer";
import toast from "react-hot-toast";

function Settings(){

const save=()=>{

toast.success("Settings Saved");

};

return(

<>

<Navbar/>

<div style={{display:"flex"}}>

<Sidebar/>

<div style={styles.main}>

<h1>

System Settings

</h1>

<div style={styles.card}>

<label>

Application Name

</label>

<input

defaultValue="DIAGNOAI"

style={styles.input}

/>

<label>

Admin Email

</label>

<input

defaultValue="admin@diagnoai.com"

style={styles.input}

/>

<label>

Prediction Threshold

</label>

<input

defaultValue="0.80"

style={styles.input}

/>

<button

onClick={save}

style={styles.button}

>

Save Settings

</button>

</div>

</div>

</div>

<Footer/>

</>

);

}

const styles={

main:{
marginLeft:"270px",
padding:"50px",
width:"100%"
},

card:{
background:"#fff",
padding:"30px",
borderRadius:"20px",
border:"3px solid gold",
maxWidth:"600px"
},

input:{
width:"100%",
padding:"15px",
marginBottom:"20px",
borderRadius:"10px",
border:"2px solid gold"
},

button:{
background:"#1976d2",
color:"#fff",
padding:"15px 30px",
border:"none",
borderRadius:"10px",
cursor:"pointer"
}

};

export default Settings;