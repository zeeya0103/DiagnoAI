def predict_disease(hb, glucose):

    if hb < 12:
        return "Anemia Risk"

    if glucose > 125:
        return "Diabetes Risk"

    return "Normal"