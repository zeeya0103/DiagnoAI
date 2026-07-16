import re


class ReportInterpreter:

    @staticmethod
    def extract_parameters(text: str):

        report = {}

        # Make OCR text easier to parse
        text = text.replace(",", ".")
        text = re.sub(r"\s+", " ", text)

        patterns = {

    "hemoglobin": r"(?:HEMOGLOBIN|Haemoglobin|Hb).*?(\d+(?:\.\d+)?)\s*g/?dL",

    "glucose": r"(?:AVERAGE BLOOD GLUCOSE|Blood Glucose|GLUCOSE|FBS|RBS).*?(\d+(?:\.\d+)?)\s*mg/?dL",

    "hba1c": r"(?:HbA1c|Glycated Hemoglobin).*?(\d+(?:\.\d+)?)",

    "cholesterol": r"(?:TOTAL CHOLESTEROL|Cholesterol).*?(\d+(?:\.\d+)?)\s*mg/?dL",

    "triglycerides": r"(?:TRIGLYCERIDES).*?(\d+(?:\.\d+)?)",

    "hdl": r"(?:HDL).*?(\d+(?:\.\d+)?)",

    "ldl": r"(?:LDL).*?(\d+(?:\.\d+)?)",

    "vldl": r"(?:VLDL).*?(\d+(?:\.\d+)?)",

    "rbc": r"(?:RBC|Red Blood Cells).*?(\d+(?:\.\d+)?)",

    "wbc": r"(?:WBC|White Blood Cells|Total WBC).*?(\d+(?:\.\d+)?)",

    "platelets": r"(?:Platelet Count|Platelets).*?(\d+(?:\.\d+)?)",

    "pcv": r"(?:PCV|Packed Cell Volume).*?(\d+(?:\.\d+)?)",

    "mcv": r"(?:MCV).*?(\d+(?:\.\d+)?)",

    "mch": r"(?:MCH).*?(\d+(?:\.\d+)?)",

    "mchc": r"(?:MCHC).*?(\d+(?:\.\d+)?)",

    "neutrophils": r"(?:Neutrophils).*?(\d+(?:\.\d+)?)",

    "lymphocytes": r"(?:Lymphocytes).*?(\d+(?:\.\d+)?)",

    "monocytes": r"(?:Monocytes).*?(\d+(?:\.\d+)?)",

    "eosinophils": r"(?:Eosinophils).*?(\d+(?:\.\d+)?)",

    "basophils": r"(?:Basophils).*?(\d+(?:\.\d+)?)",

    "creatinine": r"(?:Creatinine|Serum Creatinine).*?(\d+(?:\.\d+)?)",

    "urea": r"(?:Blood Urea|Urea).*?(\d+(?:\.\d+)?)",

    "uric_acid": r"(?:Uric Acid).*?(\d+(?:\.\d+)?)",

    "bilirubin": r"(?:Total Bilirubin|Bilirubin).*?(\d+(?:\.\d+)?)",

    "sgot": r"(?:SGOT|AST).*?(\d+(?:\.\d+)?)",

    "sgpt": r"(?:SGPT|ALT).*?(\d+(?:\.\d+)?)",

    "alkaline_phosphatase": r"(?:Alkaline Phosphatase|ALP).*?(\d+(?:\.\d+)?)",

    "albumin": r"(?:Albumin).*?(\d+(?:\.\d+)?)",

    "globulin": r"(?:Globulin).*?(\d+(?:\.\d+)?)",

    "calcium": r"(?:Calcium).*?(\d+(?:\.\d+)?)",

    "sodium": r"(?:Sodium).*?(\d+(?:\.\d+)?)",

    "potassium": r"(?:Potassium).*?(\d+(?:\.\d+)?)",

    "chloride": r"(?:Chloride).*?(\d+(?:\.\d+)?)",

    "tsh": r"(?:TSH).*?(\d+(?:\.\d+)?)",

    "t3": r"(?:T3).*?(\d+(?:\.\d+)?)",

    "t4": r"(?:T4).*?(\d+(?:\.\d+)?)"

}

        for key, pattern in patterns.items():

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                try:
                    report[key] = float(match.group(1))

                except ValueError:
                    report[key] = None

            else:
                report[key] = None

        return report


    @staticmethod
    def health_summary(report):

        summary = []

        hb = report.get("hemoglobin")
        glucose = report.get("glucose")
        cholesterol = report.get("cholesterol")

        if hb is not None:

            if hb < 12:
                summary.append("Low Hemoglobin detected. Possible Anaemia.")

            else:
                summary.append("Hemoglobin appears normal.")

        if glucose is not None:

            if glucose > 125:
                summary.append("High Blood Glucose detected. Diabetes risk.")

            else:
                summary.append("Blood glucose appears normal.")

        if cholesterol is not None:

            if cholesterol > 240:
                summary.append("High Cholesterol detected.")

            else:
                summary.append("Cholesterol level appears normal.")

        if not summary:
            summary.append("No significant abnormalities detected.")

        return summary