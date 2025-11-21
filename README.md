# Student Mental Health CGPA Predictor

## Project Overview

This project implements a complete machine learning deployment pipeline that predicts student academic performance (CGPA) based on mental health indicators. The system enables universities to identify at-risk students early and implement proactive mental health interventions and academic support programs, ultimately improving student wellbeing and success rates.

---

## Mission Statement

To use entertainment and tech, to enlighten people about societal issues and inspire solutions for a cooperative society, with a focus on addressing youth mental health in Africa through arts, culture, wildlife conservation, and technology.
---

## Dataset Information

**Source:** Kaggle - [Student Mental Health Dataset](https://www.kaggle.com/datasets/shariful07/student-mental-health)

**Description:** The dataset contains mental health survey responses from 101 university students, capturing their mental health status alongside academic performance. The data includes demographic information, course details, and self-reported mental health indicators that allow for analysis of the relationship between psychological wellbeing and academic achievement.

**Dataset Characteristics:**
- **Size:** 101 student records
- **Features:** 11 total features
- **Target Variable:** CGPA (Cumulative Grade Point Average)
- **Data Types:** Mixed (numeric and categorical)

**Features:**
1. **Age** (18-24 years) - Student's age
2. **Gender** (Male/Female) - Student's gender
3. **Course** - Field of study (Engineering, BIT, Law, etc.)
4. **Year of Study** (year 1-4) - Current academic year
5. **CGPA** - Cumulative Grade Point Average (Target Variable)
6. **Marital Status** (Yes/No) - Whether student is married
7. **Depression** (Yes/No) - Self-reported depression status
8. **Anxiety** (Yes/No) - Self-reported anxiety status
9. **Panic Attacks** (Yes/No) - Experience of panic attacks
10. **Treatment** (Yes/No) - Whether sought professional help

---

## System Architecture

The project consists of three main components:

### 1. **Machine Learning Model** (Python/Scikit-learn)
- Data preprocessing and feature engineering
- Training of multiple regression models
- Model evaluation and selection
- Model persistence for deployment

### 2. **REST API** (FastAPI)
- Serves predictions via HTTP endpoints
- Input validation using Pydantic
- CORS-enabled for cross-origin requests
- Deployed on Render cloud platform

### 3. **Mobile Application** (Flutter)
- User-friendly interface for data input
- Real-time prediction requests
- Result visualization
- Error handling and validation

---

## Model Development

### Data Preprocessing

**Handling Missing Values:**
- 1 missing value in Age column filled with median (20.5 years)
- No missing values in target variable (CGPA)

**Feature Engineering:**
- Converted CGPA ranges to numeric values:
  - "3.50 - 4.00" → 3.75
  - "3.00 - 3.49" → 3.25
  - "2.50 - 2.99" → 2.75
  - "2.00 - 2.49" → 2.25
  - "0 - 1.99" → 1.00
- Encoded categorical variables using LabelEncoder
- Standardized all features using StandardScaler

**Train-Test Split:**
- Training Set: 80% (80 samples)
- Testing Set: 20% (21 samples)
- Random State: 42 (for reproducibility)


### Model Selection Justification

**Linear Regression was selected as the best model** for the following reasons:

1. **Lowest Test MSE (0.3549):** Outperformed both tree-based models on unseen data
2. **Best Generalization:** Minimal gap between training and testing performance
3. **Stability:** Avoided overfitting that plagued Decision Tree and Random Forest
4. **Simplicity:** Linear model prevents overfitting on small dataset (101 samples)
5. **Interpretability:** Easier to understand feature contributions


---

## API Documentation

### Base URL

**Production:** `https://mobile-app-regression-ml.onrender.com`

**Swagger UI:** `https://mobile-app-regression-ml.onrender.com/docs`

### Endpoints

#### 1. Root Endpoint
```http
GET /
```
Returns API welcome message and available endpoints.

#### 2. Health Check
```http
GET /health
```
Verifies API status and model availability.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "scaler_loaded": true,
  "encoders_loaded": true
}
```

#### 3. Prediction Endpoint
```http
POST /predict
```

**Request Body:**
```json
{
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
```

**Response:**
```json
{
  "predicted_cgpa": 3.25,
  "cgpa_range": "Good (3.00 - 3.49)",
  "message": "Student is performing well academically."
}
```

### Input Validation

The API enforces strict validation using Pydantic:

- **age:** Integer, range 18-30
- **gender:** Exactly "Male" or "Female"
- **course:** String, 2-100 characters
- **year:** Exactly "year 1", "year 2", "year 3", or "year 4"
- **marital_status:** Exactly "Yes" or "No"
- **depression:** Exactly "Yes" or "No"
- **anxiety:** Exactly "Yes" or "No"
- **panic_attack:** Exactly "Yes" or "No"
- **treatment:** Exactly "Yes" or "No"

Invalid inputs return detailed error messages with HTTP 400 status.

### CORS Configuration

The API includes CORS middleware allowing cross-origin requests from any domain, enabling the Flutter mobile application to communicate with the backend.

---

## Mobile Application

### Features

- **Input Form:** 9 fields for student information and mental health status
- **Validation:** Client-side input validation before API calls
- **Prediction:** Real-time CGPA prediction via API
- **Result Display:** Color-coded results with interpretation messages
- **Error Handling:** Clear error messages for validation failures and network issues
- **Loading States:** Visual feedback during API requests
- **Responsive Design:** Works across different screen sizes and orientations

### Technology Stack

- **Framework:** Flutter 3.x
- **Language:** Dart
- **State Management:** StatefulWidget with setState
- **HTTP Client:** http package
- **UI Components:** Material Design widgets


---

## Installation & Setup

### Prerequisites

- Python 3.13+
- Flutter 3.x+
- Git

### Backend Setup (API)

1. **Clone the repository:**
```bash
git clone https://github.com/Emma-Asoliya/Mobile_App_Regression_ML.git
cd Mobile_App_Regression_ML
```

2. **Navigate to API directory:**
```bash
cd API
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the API locally:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

5. **Access Swagger UI:**
Open browser to `http://localhost:8000/docs`

### Frontend Setup (Flutter App)

1. **Navigate to Flutter directory:**
```bash
cd mobile_app_regression_analysis
```

2. **Get dependencies:**
```bash
flutter pub get
```

3. **Run the app:**
```bash
flutter run
```

**Note:** The app is configured to use the deployed API. To use local API, update the `apiUrl` in `main.dart`:
```dart
final String apiUrl = 'http://localhost:8000/predict';
```

---

## Testing

### API Testing

**Using Swagger UI:**
1. Navigate to `https://mobile-app-regression-ml.onrender.com/docs`
2. Click on `/predict` endpoint
3. Click "Try it out"
4. Modify sample data or use defaults
5. Click "Execute"
6. View response



## References

1. Student Mental Health Dataset. Kaggle. https://www.kaggle.com/datasets/shariful07/student-mental-health

2. FastAPI Documentation. https://fastapi.tiangolo.com/

3. Flutter Documentation. https://docs.flutter.dev/

4. Scikit-learn: Machine Learning in Python. https://scikit-learn.org/

5. Pydantic Documentation. https://docs.pydantic.dev/

6. Render Deployment Documentation. https://render.com/docs

7. Claude AI. https://claude.ai/new
   
## Demo Video
Link to my demo video - https://youtu.be/BiPVvBMjDss
