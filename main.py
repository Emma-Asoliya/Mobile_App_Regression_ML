"""
Mental Health CGPA Prediction API
FastAPI application for predicting student CGPA based on mental health indicators
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
import joblib
import pandas as pd
from typing import Literal
import os

# INITIALIZE FASTAPI APP

app = FastAPI(
    title="Student Mental Health CGPA Prediction API",
    description="Predicts student CGPA based on mental health indicators and demographics",
    version="1.0.0"
)

 
# CORS MIDDLEWARE (Required for Flutter app to access API)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# LOAD MODEL AND PREPROCESSING OBJECTS


try:
    model = joblib.load('best_model.pkl')
    scaler = joblib.load('scaler.pkl')
    label_encoders = joblib.load('label_encoders.pkl')
    feature_names = joblib.load('feature_names.pkl')
    print("✅ Model and preprocessing objects loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model files: {e}")
    raise


# PYDANTIC MODEL FOR INPUT VALIDATION


class StudentInput(BaseModel):
    """
    Input schema for CGPA prediction with data type and range validation
    """
    
    age: int = Field(
        ..., 
        ge=18, 
        le=30,
        description="Student age (18-30 years)",
        example=21
    )
    
    gender: Literal["Male", "Female"] = Field(
        ...,
        description="Student gender",
        example="Male"
    )
    
    course: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Course/Major name",
        example="Engineering"
    )
    
    year: Literal["year 1", "year 2", "year 3", "year 4"] = Field(
        ...,
        description="Current year of study",
        example="year 2"
    )
    
    marital_status: Literal["Yes", "No"] = Field(
        ...,
        description="Marital status (Yes=Married, No=Single)",
        example="No"
    )
    
    depression: Literal["Yes", "No"] = Field(
        ...,
        description="Do you have depression?",
        example="No"
    )
    
    anxiety: Literal["Yes", "No"] = Field(
        ...,
        description="Do you have anxiety?",
        example="Yes"
    )
    
    panic_attack: Literal["Yes", "No"] = Field(
        ...,
        description="Do you have panic attacks?",
        example="No"
    )
    
    treatment: Literal["Yes", "No"] = Field(
        ...,
        description="Did you seek specialist treatment?",
        example="No"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 21,
                "gender": "Male",
                "course": "Engineering",
                "year": "year 2",
                "marital_status": "No",
                "depression": "No",
                "anxiety": "Yes",
                "panic_attack": "No",
                "treatment": "No"
            }
        }


# PYDANTIC MODEL FOR OUTPUT


class PredictionOutput(BaseModel):
    """
    Output schema for prediction response
    """
    predicted_cgpa: float = Field(
        ...,
        description="Predicted CGPA value",
        example=3.25
    )
    cgpa_range: str = Field(
        ...,
        description="CGPA interpretation range",
        example="Good (3.00 - 3.49)"
    )
    message: str = Field(
        ...,
        description="Interpretation message",
        example="Student is performing well academically"
    )


# HELPER FUNCTION: CGPA INTERPRETATION


def interpret_cgpa(cgpa: float) -> tuple:
    """
    Convert numeric CGPA to range and message
    
    Parameters:
    -----------
    cgpa : float
        Predicted CGPA value
        
    Returns:
    --------
    tuple : (range_string, message)
    """
    if cgpa >= 3.50:
        return "Excellent (3.50 - 4.00)", "Student is performing excellently! Keep up the great work."
    elif cgpa >= 3.00:
        return "Good (3.00 - 3.49)", "Student is performing well academically."
    elif cgpa >= 2.50:
        return "Average (2.50 - 2.99)", "Student is performing at an average level. Some improvement possible."
    elif cgpa >= 2.00:
        return "Below Average (2.00 - 2.49)", "Student may need academic support and intervention."
    else:
        return "Poor (0.00 - 1.99)", "Student requires immediate academic and mental health support."

# API ENDPOINTS

@app.get("/")
async def root():
    """
    Root endpoint - API welcome message
    """
    return {
        "message": "Welcome to Student Mental Health CGPA Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict (POST)",
            "health": "/health (GET)",
            "docs": "/docs (Swagger UI)",
            "redoc": "/redoc (ReDoc)"
        }
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API is running
    """
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "encoders_loaded": label_encoders is not None
    }

@app.post("/predict", response_model=PredictionOutput)
async def predict_cgpa(student: StudentInput):
    """
    Predict student CGPA based on mental health and demographic information
    
    Parameters:
    -----------
    student : StudentInput
        Student information including age, gender, course, year, and mental health status
        
    Returns:
    --------
    PredictionOutput
        Predicted CGPA value with interpretation
    """
    
    try:
        # Create input dictionary matching training feature names
        input_data = {
            'Age': student.age,
            'Choose your gender': student.gender,
            'What is your course?': student.course,
            'Your current year of Study': student.year,
            'Marital status': student.marital_status,
            'Do you have Depression?': student.depression,
            'Do you have Anxiety?': student.anxiety,
            'Do you have Panic attack?': student.panic_attack,
            'Did you seek any specialist for a treatment?': student.treatment
        }
        
        # Convert to DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Encode categorical variables
        for col in label_encoders.keys():
            if col in input_df.columns:
                try:
                    input_df[col] = label_encoders[col].transform([str(input_data[col])])[0]
                except ValueError as e:
                    # Handle unseen categories
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid value for {col}: {input_data[col]}. Must be one of the categories in training data."
                    )
        
        # Ensure correct column order
        input_df = input_df[feature_names]
        
        # Scale the input
        input_scaled = scaler.transform(input_df)
        
        # Make prediction
        prediction = model.predict(input_scaled)
        predicted_cgpa = float(prediction[0])
        
        # Round to 2 decimal places
        predicted_cgpa = round(predicted_cgpa, 2)
        
        # Ensure CGPA is within valid range (0-4.0)
        predicted_cgpa = max(0.0, min(4.0, predicted_cgpa))
        
        # Get interpretation
        cgpa_range, message = interpret_cgpa(predicted_cgpa)
        
        return PredictionOutput(
            predicted_cgpa=predicted_cgpa,
            cgpa_range=cgpa_range,
            message=message
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )

# RUN THE APP (for local testing)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)