from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import shap
import os

from backend.utils.suggestions import generate_suggestions


# Load models
BASE_PATH = "/Users/rutujashingate/Desktop/sleep-ml-project/backend/models"

survey_model_path = f"{BASE_PATH}/sleep_quality_model.pkl"
smartwatch_model_path = f"{BASE_PATH}/smartwatch_model.pkl"

if not os.path.exists(survey_model_path) or not os.path.exists(smartwatch_model_path):
    raise FileNotFoundError("❌ Model files missing in backend/models")

survey_model = joblib.load(survey_model_path)
smartwatch_model = joblib.load(smartwatch_model_path)


# FastAPI App

app = FastAPI(
    title="Sleep Prediction API",
    description="Predict sleep quality using survey & smartwatch data",
    version="1.0"
)


# CORS (Frontend → Backend)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Schemas

class SurveyInput(BaseModel):
    Sleep_Duration: float
    Stress_Level: float
    Physical_Activity_Level: float
    Heart_Rate: float
    Daily_Steps: int
    Age: int
    Gender: str
    Occupation: str
    BMI_Category: str
    Sleep_Disorder: str
    Systolic_BP: float
    Diastolic_BP: float

class SmartwatchInput(BaseModel):
    age: int
    gender: str
    stress_score: float
    screen_time_before_bed_min: float
    step_count_day: int
    sleep_stage_deep_pct: float
    sleep_stage_light_pct: float
    sleep_efficiency: float



# Survey Prediction

@app.post("/predict_survey")
def predict_survey(data: SurveyInput):
    input_df = pd.DataFrame([data.dict()])

    input_df.rename(columns={
        "Sleep_Duration": "Sleep Duration",
        "Stress_Level": "Stress Level",
        "Physical_Activity_Level": "Physical Activity Level",
        "Heart_Rate": "Heart Rate",
        "Daily_Steps": "Daily Steps",
        "BMI_Category": "BMI Category",
        "Sleep_Disorder": "Sleep Disorder",
    }, inplace=True)

    try:
        pred = survey_model.predict(input_df)[0]
        return {"prediction": round(pred, 2), "model": "Survey"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Smartwatch Prediction (WITH DEFAULT FILLING)

@app.post("/predict_smartwatch")
def predict_smartwatch(data: SmartwatchInput):

    user_input = data.dict()

    
    model_features = smartwatch_model.feature_names_in_


    defaults = {
        'sleep_efficiency': 80.0,
        'stress_score': 5.0,
        'sleep_stage_deep_pct': 15.0,
        'sleep_stage_rem_pct': 20.0,
        'sleep_stage_light_pct': 50.0,
        'sleep_stage_awake_pct': 15.0,
        'caffeine_mg': 100.0,
        'bedtime_consistency_std_min': 30.0,
        'hrv_rmssd_ms': 25.0,
        'room_humidity_pct': 40.0,
        'step_count_day': 5000,
        'ambient_noise_db': 35.0,
        'height_cm': 170.0,
        'room_temperature_c': 22.0,
        'age': 25,
        'screen_time_before_bed_min': 45.0,
        'activity_before_bed_min': 20.0,
        'weight_kg': 65.0,
        'respiration_rate_bpm': 15.0,
        'jetlag_hours': 0.0,
    }

  
    final_input = {}
    for col in model_features:
        final_input[col] = user_input.get(col, defaults[col])

    input_df = pd.DataFrame([final_input])

    print("✅ FINAL INPUT ORDER:", input_df.columns.tolist())

    try:
        # Prediction
        pred = smartwatch_model.predict(input_df)[0]

        # SHAP
        explainer = shap.Explainer(smartwatch_model)
        shap_values = explainer(input_df)

        top_features = sorted(
            zip(input_df.columns, shap_values.values[0]),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:5]

        feature_impact = [
            {"feature": f, "impact": round(float(v), 4)}
            for f, v in top_features
        ]

        suggestions = generate_suggestions(user_input)

        return {
            "prediction": round(pred, 2),
            "important_features": feature_impact,
            "suggestions": suggestions
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

