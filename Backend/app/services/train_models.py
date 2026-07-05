import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

# Train Anemia Model
anemia = pd.read_csv("ml/anemia_dataset.csv")
X = anemia[["hemoglobin", "age", "gender"]]
y = anemia["anemia"]

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "ml/anemia_model.pkl")

# Train Diabetes Model
diabetes = pd.read_csv("ml/diabetes_dataset.csv")
X = diabetes[["glucose", "bmi", "age"]]
y = diabetes["diabetes"]

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "ml/diabetes_model.pkl")

print("Models trained successfully!")