from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import pandas as pd

# Load model and encoders
rf = joblib.load("rf_attrition_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")

app = FastAPI(title="Employee Attrition Predictor")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic input model with example
class EmployeeFeatures(BaseModel):
    MonthlyIncome: int = Field(..., example=35000)
    Age: int = Field(..., example=29)
    TotalWorkingYears: int = Field(..., example=5)
    DistanceFromHome: int = Field(..., example=10)
    PercentSalaryHike: int = Field(..., example=12)
    OverTime: str = Field(..., example="Yes", description="Yes or No")
    YearsAtCompany: int = Field(..., example=2)
    NumCompaniesWorked: int = Field(..., example=3)
    PerformanceRating: int = Field(..., example=3)

@app.post("/predict")
def predict_attrition(employee: EmployeeFeatures):
    # Convert to DataFrame for processing
    df = pd.DataFrame([employee.dict()])

    # Encode categorical variables
    for col, le in label_encoders.items():
        if col in df.columns:
            df[col] = le.transform(df[col])

    # Predict
    pred = rf.predict(df)[0]
    label = label_encoders['Attrition'].inverse_transform([pred])[0]
    prob = rf.predict_proba(df)[0][1]

    return {
        "predicted_attrition": label,
        "probability_of_leaving": f"{prob:.2%}"
    }
