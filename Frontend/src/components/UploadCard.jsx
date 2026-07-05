import { useState } from "react";
import axios from "../api/axios";
import toast from "react-hot-toast";
import { FaCloudUploadAlt } from "react-icons/fa";

function UploadCard(){

const[file,setFile]=useState(null);

const upload=async()=>{

if(!file){

toast.error("Choose PDF");

return;

}

const formData=new FormData();

formData.append("file",file);

try{

await axios.post(

"/reports/upload",

formData,

{

headers:{

"Content-Type":"multipart/form-data",

Authorization:`Bearer ${localStorage.getItem("token")}`

}

}

);

toast.success("Report Uploaded");

}

catch{

toast.error("Upload Failed");

}

};

return(

<div className="card">

<h2 style={{color:"#d62828"}}>

Upload Blood Report

</h2>

<div

style={{

border:"3px dashed #1976d2",

padding:"40px",

borderRadius:"15px",

textAlign:"center",

marginTop:"20px"

}}

>

<FaCloudUploadAlt

size={80}

color="#1976d2"

/>

<input

type="file"

accept=".pdf"

onChange={(e)=>setFile(e.target.files[0])}

/>

<button

className="primary-btn"

style={{marginTop:"20px"}}

onClick={upload}

>

Upload Report

</button>

</div>

</div>

);

}

export default UploadCard;