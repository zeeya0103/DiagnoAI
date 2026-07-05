import { useState } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Footer from "../components/Footer";

import axios from "axios";

import { motion } from "framer-motion";

function Chatbot(){

const[input,setInput]=useState("");

const[messages,setMessages]=useState([]);

const send=async()=>{

if(input==="") return;

const userMessage={
sender:"You",
text:input
};

setMessages(prev=>[...prev,userMessage]);

try{

const res=await axios.post(

"http://127.0.0.1:8000/chatbot",

{

message:input

},

{

headers:{

Authorization:`Bearer ${localStorage.getItem("token")}`

}

}

);

setMessages(prev=>[

...prev,

{

sender:"AI",

text:res.data.reply

}

]);

}

catch{

setMessages(prev=>[

...prev,

{

sender:"AI",

text:"Unable to connect."

}

]);

}

setInput("");

};

return(

<>

<Navbar/>

<div style={styles.container}>

<Sidebar/>

<div style={styles.chat}>

<h1 style={styles.heading}>

DIAGNOAI Assistant

</h1>

<div style={styles.box}>

{

messages.map((msg,index)=>(

<motion.div

key={index}

initial={{opacity:0}}

animate={{opacity:1}}

style={

msg.sender==="You"

?

styles.user

:

styles.ai

}

>

<b>

{msg.sender}

</b>

<br/>

{msg.text}

</motion.div>

))

}

</div>

<div style={styles.inputArea}>

<input

value={input}

onChange={(e)=>setInput(e.target.value)}

placeholder="Ask about your report..."

style={styles.input}

/>

<button

onClick={send}

style={styles.button}

>

Send

</button>

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
background:"#f8f9fa"
},

chat:{
marginLeft:"270px",
padding:"50px",
width:"100%"
},

heading:{
color:"#d62828",
marginBottom:"25px"
},

box:{
height:"500px",
overflowY:"auto",
background:"#fff",
padding:"25px",
borderRadius:"18px",
border:"3px solid gold"
},

user:{
background:"#1976d2",
color:"#fff",
padding:"15px",
borderRadius:"12px",
marginBottom:"15px",
marginLeft:"120px"
},

ai:{
background:"#fff8dc",
padding:"15px",
borderRadius:"12px",
marginBottom:"15px",
border:"2px solid gold",
marginRight:"120px"
},

inputArea:{
display:"flex",
marginTop:"20px",
gap:"15px"
},

input:{
flex:1,
padding:"15px",
borderRadius:"10px",
border:"2px solid gold",
fontSize:"16px"
},

button:{
background:"#d62828",
color:"#fff",
padding:"15px 35px",
border:"none",
borderRadius:"10px",
cursor:"pointer",
fontWeight:"bold"
}

};

export default Chatbot;