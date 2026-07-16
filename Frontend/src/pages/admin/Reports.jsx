import { useEffect, useState } from "react";
import Navbar from "../../components/Navbar";
import Sidebar from "../../components/Sidebar";
import Footer from "../../components/Footer";
import axios from "axios";
import toast from "react-hot-toast";
import { motion } from "framer-motion";
import {
  FaTrash,
  FaDownload,
  FaSearch,
  FaFileMedical
} from "react-icons/fa";


const API_URL = "https://diagnoai-1-xywq.onrender.com";


function Reports() {

  const [reports, setReports] = useState([]);
  const [search, setSearch] = useState("");


  useEffect(() => {
    loadReports();
  }, []);



  const loadReports = async () => {

    try {

      const res = await axios.get(
        `${API_URL}/admin/reports`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`
          }
        }
      );

      setReports(res.data);

    } catch (error) {

      console.log(error);
      toast.error("Unable to Load Reports");

    }

  };



  const deleteReport = async(id)=>{

    if(!window.confirm("Delete this report?")) return;


    try{

      await axios.delete(

        `${API_URL}/admin/reports/${id}`,

        {
          headers:{
            Authorization:`Bearer ${localStorage.getItem("token")}`
          }
        }

      );


      toast.success("Report Deleted");

      loadReports();


    }

    catch(error){

      console.log(error);
      toast.error("Delete Failed");

    }

  };



  const filtered = reports.filter((r)=>

      r.patient_name?.toLowerCase()
      .includes(search.toLowerCase())

      ||

      r.file_name?.toLowerCase()
      .includes(search.toLowerCase())

  );



  return (

    <>


      <Navbar/>


      <div style={styles.container}>


        <Sidebar/>


        <div style={styles.content}>


          <h1 style={styles.heading}>
            Report Management
          </h1>



          <div style={styles.searchBox}>


            <FaSearch/>


            <input

              placeholder="Search Patient / Report..."

              style={styles.input}

              value={search}

              onChange={(e)=>setSearch(e.target.value)}

            />


          </div>





          <table style={styles.table}>


            <thead>


              <tr>

                <th>Patient</th>

                <th>Report</th>

                <th>Disease</th>

                <th>Risk</th>

                <th>Date</th>

                <th>Actions</th>


              </tr>


            </thead>



            <tbody>


            {


              filtered.map((item,index)=>(


                <motion.tr

                key={index}

                whileHover={{
                  background:"#fff8dc"
                }}

                >



                  <td>
                    {item.patient_name}
                  </td>



                  <td>


                    <FaFileMedical color="#d62828"/>

                    {" "}

                    {item.file_name}


                  </td>



                  <td>
                    {item.prediction}
                  </td>



                  <td>
                    {item.risk}
                  </td>



                  <td>
                    {item.created_at}
                  </td>



                  <td>


                    <button

                      style={styles.download}

                    >

                      <FaDownload/>

                    </button>




                    <button

                      style={styles.delete}

                      onClick={()=>deleteReport(item.id)}

                    >

                      <FaTrash/>

                    </button>



                  </td>




                </motion.tr>



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


container:{

display:"flex",

background:"#f5f5f5",

minHeight:"100vh"

},



content:{

marginLeft:"270px",

width:"100%",

padding:"40px"

},



heading:{

fontSize:"38px",

color:"#d62828",

marginBottom:"30px"

},



searchBox:{

display:"flex",

alignItems:"center",

background:"#fff",

padding:"12px 20px",

borderRadius:"12px",

border:"3px solid gold",

marginBottom:"30px",

maxWidth:"500px"

},



input:{

border:"none",

outline:"none",

marginLeft:"10px",

fontSize:"16px",

width:"100%"

},



table:{

width:"100%",

background:"#fff",

borderCollapse:"collapse",

border:"3px solid gold",

borderRadius:"15px",

overflow:"hidden"

},



download:{

background:"#1976d2",

color:"#fff",

border:"none",

padding:"10px 15px",

borderRadius:"8px",

cursor:"pointer",

marginRight:"10px"

},



delete:{

background:"#d62828",

color:"#fff",

border:"none",

padding:"10px 15px",

borderRadius:"8px",

cursor:"pointer"

}



};



export default Reports;