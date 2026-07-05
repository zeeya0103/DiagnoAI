import {
FaFileMedical,
FaHeartbeat,
FaTint
} from "react-icons/fa";

function ReportCard({report}){

return(

<div className="card">

<FaFileMedical
size={55}
color="#d62828"
/>

<h2>

{report.file_name}

</h2>

<p>

Disease:
<b>

{report.prediction}

</b>

</p>

<p>

Risk:

<span
style={{
color:
report.risk==="High"
?"red"
:"green"
}}
>

{report.risk}

</span>

</p>

<hr
style={{
margin:"15px 0"
}}
/>

<p>

<FaHeartbeat color="red"/>

 Hb :
 {report.hemoglobin}

</p>

<p>

<FaTint color="#1976d2"/>

 Glucose :
 {report.glucose}

</p>

<p>

Cholesterol :
{report.cholesterol}

</p>

</div>

);

}

export default ReportCard;