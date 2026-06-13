# app/engine/ai_analyzer.py
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def generate_health_analysis(extracted_data: dict) -> dict:
    """
    Assembles complete diagnostic data sets. Falls back gracefully to local calculations
    if cloud infrastructure runs into network issues or API quota constraints.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Check for anomalies using high-speed deterministic processing logic
    anomalies = []
    if extracted_data["glucose"] > 100: anomalies.append("Elevated Fasting Glucose (Diabetes risk indicator)")
    if extracted_data["hemoglobin"] < 12.0: anomalies.append("Low Hemoglobin (Anemia tracking indicated)")
    if extracted_data["cholesterol"] >= 200: anomalies.append("High Cholesterol profile detected")
    if extracted_data["wbc"] > 11.0: anomalies.append("Elevated Leukocytes count (Active infection indicator)")

    status = "Action Required" if anomalies else "Healthy"
    risk_level = "High" if len(anomalies) >= 2 else ("Moderate" if anomalies else "Low")
    
    # Base response payload
    fallback_analysis = {
        "status": status,
        "risk_level": risk_level,
        "explanation": f"System scan parsed metrics dynamically. Detected variations: {', '.join(anomalies) if anomalies else 'None'}.",
        "precautions": "Maintain regular monitoring protocols, limit simple glycemic intakes, and track metrics weekly.",
        "suggestions": "Schedule an evaluation loop with your clinical primary care provider to review anomalous vectors."
    }

    if not api_key:
        return fallback_analysis

    try:
        # Deploy cloud-based AI structural rendering if authorization keys are available
        client = OpenAI(api_key=api_key)
        prompt = f"Analyze these extracted blood report metrics: {json.dumps(extracted_data)}. Generate explanations, risks, precautions, and medical consultation notes in a clean JSON format matching this dictionary framework: {json.dumps(fallback_analysis)}"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception:
        return fallback_analysis