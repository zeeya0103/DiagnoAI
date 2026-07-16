import { useState } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Footer from "../components/Footer";
import ReportCard from "../components/ReportCard";

import { motion } from "framer-motion";
import { FaCloudUploadAlt, FaFileMedical } from "react-icons/fa";
import axios from "axios";
import toast from "react-hot-toast";

function UploadReport() {

    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);

    // NEW
    const [report, setReport] = useState(null);

    const upload = async () => {

        if (!file) {
            toast.error("Select a PDF Report");
            return;
        }

        const data = new FormData();
        data.append("file", file);

        try {

            setLoading(true);

            const res = await axios.post(

                "https://diagnoai-1-xywq.onrender.com/reports/upload",

                data,

                {

                    headers: {

                        Authorization: `Bearer ${localStorage.getItem("token")}`,

                        "Content-Type": "multipart/form-data"

                    }

                }

            );

            toast.success("Report Uploaded Successfully");

            console.log(res.data);

            // SAVE RESPONSE
            setReport({

                file_name: file.name,

                prediction: res.data.prediction,

                risk: res.data.risk,

                parameters: res.data.parameters,

                summary: res.data.summary

            });

        }

        catch (err) {

            console.log(err);

            toast.error("Upload Failed");

        }

        finally {

            setLoading(false);

        }

    };

    return (

        <>

            <Navbar />

            <div style={styles.container}>

                <Sidebar />

                <div style={styles.content}>

                    <motion.div

                        initial={{ opacity: 0, y: 40 }}

                        animate={{ opacity: 1, y: 0 }}

                        style={styles.card}

                    >

                        <FaCloudUploadAlt

                            size={80}

                            color="#1976d2"

                        />

                        <h1 style={styles.heading}>

                            Upload Blood Report

                        </h1>

                        <p style={styles.text}>

                            Supported Format : PDF

                        </p>

                        <label style={styles.uploadBox}>

                            <input

                                type="file"

                                accept=".pdf"

                                hidden

                                onChange={(e) => setFile(e.target.files[0])}

                            />

                            <FaFileMedical

                                size={60}

                                color="#d62828"

                            />

                            <h3>

                                Click to Select PDF

                            </h3>

                        </label>

                        {

                            file && (

                                <div style={styles.filename}>

                                    {file.name}

                                </div>

                            )

                        }

                        <button

                            onClick={upload}

                            style={styles.button}

                        >

                            {

                                loading

                                    ?

                                    "Uploading..."

                                    :

                                    "Upload Report"

                            }

                        </button>

                    </motion.div>

                    {/* SHOW AI RESULT */}

                    {

                        report && (

                            <div style={{ marginTop: "40px" }}>

                                <ReportCard report={report} />

                            </div>

                        )

                    }

                </div>

            </div>

            <Footer />

        </>

    );

}

const styles = {

    container: {

        display: "flex",

        background: "#f8f9fa"

    },

    content: {

        marginLeft: "270px",

        width: "100%",

        padding: "60px"

    },

    card: {

        background: "#fff",

        border: "3px solid gold",

        padding: "40px",

        borderRadius: "20px",

        maxWidth: "700px",

        margin: "auto",

        textAlign: "center",

        boxShadow: "0 8px 25px rgba(0,0,0,.08)"

    },

    heading: {

        marginTop: "20px",

        color: "#d62828"

    },

    text: {

        marginBottom: "30px"

    },

    uploadBox: {

        display: "block",

        padding: "50px",

        border: "3px dashed #1976d2",

        borderRadius: "20px",

        cursor: "pointer",

        background: "#fafafa"

    },

    filename: {

        marginTop: "20px",

        fontWeight: "bold",

        color: "#1976d2"

    },

    button: {

        marginTop: "30px",

        background: "#1976d2",

        color: "#fff",

        padding: "15px 35px",

        border: "none",

        borderRadius: "10px",

        fontSize: "18px",

        fontWeight: "bold",

        cursor: "pointer"

    }

};

export default UploadReport;