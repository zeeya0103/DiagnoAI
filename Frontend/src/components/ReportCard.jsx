import {
    FaFileMedical
} from "react-icons/fa";

function ReportCard({ report }) {

    return (

        <div className="card">

            <FaFileMedical
                size={55}
                color="#d62828"
            />

            <h2>
                {report.file_name}
            </h2>

            <p>
                Disease :
                <b>
                    {report.prediction}
                </b>
            </p>

            <p>
                Risk :
                <span
                    style={{
                        color:
                            report.risk === "High"
                                ? "red"
                                : report.risk === "Moderate"
                                ? "orange"
                                : "green",
                        fontWeight: "bold"
                    }}
                >
                    {report.risk}
                </span>
            </p>

        </div>

    );

}

export default ReportCard;