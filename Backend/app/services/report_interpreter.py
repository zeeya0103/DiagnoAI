import re


class ReportInterpreter:

    @staticmethod
    def extract_parameters(text: str):

        report = {}

        patterns = {
            "hemoglobin": r"(?:Hemoglobin|Hb)\s*[:\-]?\s*(\d+\.?\d*)",
            "glucose": r"(?:Glucose|Blood Glucose)\s*[:\-]?\s*(\d+\.?\d*)",
            "cholesterol": r"(?:Cholesterol|Total Cholesterol)\s*[:\-]?\s*(\d+\.?\d*)",
            "platelets": r"(?:Platelets)\s*[:\-]?\s*(\d+)",
            "wbc": r"(?:WBC|White Blood Cells)\s*[:\-]?\s*(\d+)",
            "rbc": r"(?:RBC|Red Blood Cells)\s*[:\-]?\s*(\d+\.?\d*)",
            "creatinine": r"(?:Creatinine)\s*[:\-]?\s*(\d+\.?\d*)",
            "urea": r"(?:Urea)\s*[:\-]?\s*(\d+\.?\d*)",
            "bilirubin": r"(?:Bilirubin)\s*[:\-]?\s*(\d+\.?\d*)"
        }

        for key, pattern in patterns.items():

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:
                report[key] = float(match.group(1))
            else:
                report[key] = None

        return report

    @staticmethod
    def health_summary(report):

        summary = []

        hb = report.get("hemoglobin")
        glucose = report.get("glucose")
        cholesterol = report.get("cholesterol")

        if hb:

            if hb < 12:
                summary.append(
                    "Low Hemoglobin detected. Possible Anemia."
                )

            else:
                summary.append(
                    "Hemoglobin appears normal."
                )

        if glucose:

            if glucose > 125:
                summary.append(
                    "High Blood Glucose detected. Diabetes risk."
                )

            else:
                summary.append(
                    "Blood glucose appears normal."
                )

        if cholesterol:

            if cholesterol > 240:
                summary.append(
                    "High Cholesterol detected."
                )

            else:
                summary.append(
                    "Cholesterol level appears normal."
                )

        if not summary:
            summary.append("No significant abnormalities detected.")

        return summary