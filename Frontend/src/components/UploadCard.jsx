import { useState } from "react";
import axios from "../api/axios";
import toast from "react-hot-toast";
import { FaCloudUploadAlt } from "react-icons/fa";

function UploadCard() {

    const [file, setFile] = useState(null);

    const [result, setResult] = useState(null);

    const upload = async () => {

        if (!file) {

            toast.error("Choose PDF");

            return;

        }

        const formData = new FormData();

        formData.append("file", file);

        try {

            const res = await axios.post(

                "/reports/upload",

                formData,

                {

                    headers: {

                        "Content-Type": "multipart/form-data",

                        Authorization: `Bearer ${localStorage.getItem("token")}`

                    }

                }

            );

            setResult(res.data);

            toast.success("Report Uploaded Successfully");

        }

        catch (err) {

            console.log(err);

            toast.error("Upload Failed");

        }

    };

    return (

        <div className="card">

            <h2 style={{ color: "#d62828" }}>
                Upload Blood Report
            </h2>

            <div
                style={{
                    border: "3px dashed #1976d2",
                    padding: "40px",
                    borderRadius: "15px",
                    textAlign: "center",
                    marginTop: "20px"
                }}
            >

                <FaCloudUploadAlt
                    size={80}
                    color="#1976d2"
                />

                <br /><br />

                <input
                    type="file"
                    accept=".pdf"
                    onChange={(e) => setFile(e.target.files[0])}
                />

                <br />

                <button
                    className="primary-btn"
                    style={{ marginTop: "20px" }}
                    onClick={upload}
                >
                    Upload Report
                </button>

            </div>

            {result && (

                <div
                    style={{
                        marginTop: "30px",
                        background: "#fff",
                        border: "3px solid gold",
                        borderRadius: "15px",
                        padding: "25px",
                        boxShadow: "0 5px 15px rgba(0,0,0,.1)"
                    }}
                >

                    <h2 style={{ color: "#d62828" }}>
                        AI Analysis Result
                    </h2>

                    <p>
                        <b>Disease:</b> {result.prediction}
                    </p>

                    <p>
                        <b>Risk:</b> {result.risk}
                    </p>

                    <h3>Extracted Parameters</h3>

                    <table
                        style={{
                            width: "100%",
                            borderCollapse: "collapse"
                        }}
                    >
                        <tbody>

                            {Object.entries(result.parameters).map(([key, value]) => (

                                <tr key={key}>
                                    <td
                                        style={{
                                            padding: "8px",
                                            borderBottom: "1px solid #ddd"
                                        }}
                                    >
                                        <b>{key}</b>
                                    </td>

                                    <td
                                        style={{
                                            padding: "8px",
                                            borderBottom: "1px solid #ddd"
                                        }}
                                    >
                                        {value ?? "Not Found"}
                                    </td>
                                </tr>

                            ))}

                        </tbody>
                    </table>

                    <h3 style={{ marginTop: "20px" }}>
                        Health Summary
                    </h3>

                    <ul>

                        {result.summary.map((item, index) => (

                            <li key={index}>
                                {item}
                            </li>

                        ))}

                    </ul>

                </div>

            )}

        </div>

    );

}

export default UploadCard;