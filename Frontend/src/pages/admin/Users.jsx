import { useEffect,useState } from "react";
import Navbar from "../../components/Navbar";
import Sidebar from "../../components/Sidebar";
import Footer from "../../components/Footer";
import axios from "axios";

function Users(){

const[users,setUsers]=useState([]);

useEffect(()=>{

loadUsers();

},[]);

const loadUsers=async()=>{

try{

const res=await axios.get(

"https://diagnoai-1-xywq.onrender.com/admin/users",

{

headers:{
Authorization:`Bearer ${localStorage.getItem("token")}`
}

}

);

setUsers(res.data);

}

catch{}

};

return(

<>

<Navbar/>

<div style={styles.container}>

<Sidebar/>

<div style={styles.main}>

<h1>

Users

</h1>

<table style={styles.table}>

<thead>

<tr>

<th>Name</th>

<th>Email</th>

<th>Role</th>

</tr>

</thead>

<tbody>

{

users.map((u,index)=>(

<tr key={index}>

<td>{u.name}</td>

<td>{u.email}</td>

<td>{u.role}</td>

</tr>

))

}

</tbody>

</table>

</div>

</div>

<Footer/>

</>

);

}

const styles={

container:{display:"flex"},

main:{
marginLeft:"270px",
padding:"40px",
width:"100%"
},

table:{
width:"100%",
background:"#fff",
border:"3px solid gold",
borderCollapse:"collapse"
}

};

export default Users;