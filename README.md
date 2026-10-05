<div align="center">

# 🔍 FinSight AI

### Intelligent Financial Statement Analytics & Cash Flow Forecasting Platform

*"See Beyond the Numbers."*

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&logoColor=white)](https://postgresql.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.17-FF6F00?style=flat&logo=tensorflow&logoColor=white)](https://tensorflow.org)

</div>

---

## 🌐 Live Demo

| Service | URL | Status |
|---------|-----|--------|
| **🖥️ Frontend (Main App)** | [finsight-frontend-laxo.onrender.com](https://finsight-frontned.onrender.com/) | 🟢 Live |
| **⚙️ Backend API** | [finsight-backend-ljuh.onrender.com](https://finsight-backend-na64.onrender.com/) | 🟢 Live |
| **📚 API Documentation** | [finsight-backend-ljuh.onrender.com/docs](https://finsight-backend-na64.onrender.com/docs) | 🟢 Live |

> ⚠️ **Note:** Free tier on Render spins down after 15 minutes of inactivity. The first request takes 30–60 seconds to wake up.

**Register your own account** by clicking "Create an account" on the login page.

---

## 📖 Overview

**FinSight AI** is an intelligent financial analytics platform that transforms raw financial statements into actionable, explainable business intelligence. It combines automated ratio analysis, machine learning-based cash flow forecasting, anomaly detection, explainable AI, and natural-language recommendations into one unified web application.

Built as a final-year MCA project demonstrating the practical application of AI in financial decision-making.

---

## ✨ Key Features

### 🧠 Intelligent Analysis
- Automated financial ratio computation (7 core ratios)
- **Financial Health Score** (0–100) with risk classification
- Trend analysis across 6 key metrics

### 🤖 Multi-Model ML Forecasting
- **Random Forest** — Best overall performer (MAE 963)
- **XGBoost** — Gradient boosting
- **Linear Regression** — Statistical baseline
- **LSTM** — Deep learning time-series (TensorFlow)
- **Prophet** — Time-series with confidence intervals

### 🛡️ Anomaly Detection
- **Isolation Forest** — ML-based outlier detection
- **Z-Score Analysis** — Statistical anomaly detection

### 🔍 Explainable AI (XAI)
- **SHAP** — Global feature importance
- **LIME** — Local prediction explanations
- **Natural language summary** of predictions

### 📊 Visualization & Reporting
- Interactive dashboards with **Recharts** + **Plotly**
- **PDF report export**
- **Excel report export** (multi-sheet)
- 3D animated hero scenes (React Three Fiber)

### 🔐 Security & Infrastructure
- **JWT authentication** with bcrypt password hashing
- **PostgreSQL** production database
- **CSV + Excel upload** with client-side validation
- Full **REST API** with OpenAPI/Swagger docs

---

## 🏗️ Architecture



┌─────────────────────────────────────────────────────────────┐
│ USER BROWSER │
│ https://finsight-frontend-laxo.onrender.com │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ React 18 + Vite + Recharts + Plotly + Three.js │ │
│ └──────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
│ HTTPS + JWT
▼
┌─────────────────────────────────────────────────────────────┐
│ FastAPI BACKEND │
│ https://finsight-backend-ljuh.onrender.com │
│ ┌──────────────┬──────────────┬───────────────────────┐ │
│ │ Auth (JWT) │ Ratio Eng. │ ML Prediction Engine │ │
│ ├──────────────┼──────────────┼───────────────────────┤ │
│ │ Anomaly Det │ XAI (SHAP) │ Report Generator │ │
│ └──────────────┴──────────────┴───────────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
│ SQLAlchemy ORM
▼
┌─────────────────────────────────────────────────────────────┐
│ PostgreSQL 16 (Render Managed) │
│ Users • Companies • Statements • Predictions • Reports │
└─────────────────────────────────────────────────────────────┘






---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18, Vite, React Router, Recharts, Plotly, React Three Fiber |
| **Backend** | Python 3.11, FastAPI, Pydantic v2, SQLAlchemy 2.0 |
| **Database** | PostgreSQL 16, psycopg 3 |
| **ML / DL** | scikit-learn, XGBoost, TensorFlow 2.17 (LSTM), Prophet |
| **XAI** | SHAP, LIME |
| **Data** | pandas, NumPy, openpyxl, XlsxWriter |
| **Auth** | python-jose (JWT), bcrypt |
| **Reporting** | fpdf2 (PDF), XlsxWriter (Excel) |
| **Deployment** | Render (Backend, Frontend, PostgreSQL) |
| **Dev Tools** | VS Code, Jupyter, Git, Postman |

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL 16
- Git

### 1. Clone the repository

```bash
git clone https://github.com/dogga777/finance-ai.git
cd finance-ai


#2. Backend setup

cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt

# Create .env file in backend/:

APP_NAME=FinSight AI
API_V1_PREFIX=/api/v1
SECRET_KEY=change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DATABASE_URL=postgresql+psycopg://finsight:Chandra_77@localhost:5432/finsight
MODEL_DIR=./app/ml/artifacts
UPLOAD_DIR=./uploads
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Run backend:
uvicorn app.main:app --reload
Backend: http://127.0.0.1:8000
API Docs: http://127.0.0.1:8000/docs

# 3. Frontend setup
cd ../frontend
npm install
npm run dev
Frontend at http://localhost:3000

# 📡 API Endpoints

# Auth

Method	Endpoint	            Description

POST	/api/v1/auth/register	Create new user
POST	/api/v1/auth/login	    Get JWT token
GET  	/api/v1/auth/me	        Current user info

# Core
Method       	Endpoint	      Description   

POST     	/api/v1/companies	  Create company
GET	       /api/v1/companies	  List companies
POST  /api/v1/statements/{id}/bulk	Bulk upload statements
GET	    /api/v1/analysis/{id}	  Ratios + Health Score
POST	/api/v1/predictions	    Cash flow forecast
GET	   /api/v1/anomalies/{id}	Detect anomalies
GET	  /api/v1/reports/{id}	    Full report JSON
GET	  /api/v1/reports/{id}/pdf  	Download PDF



# Advanced ML

Method         Endpoint	              Description

GET	    /api/v1/advanced/predict/lstm/{id}	LSTM forecast
GET	   /api/v1/advanced/predict/prophet/{id}	Prophet forecast
GET	   /api/v1/advanced/compare/{id}	Compare all models
GET  	/api/v1/advanced/trends/{id}	Trend analysis
GET	  /api/v1/advanced/zscore/{id}	Z-Score anomalies
GET	   /api/v1/advanced/lime/{id}	LIME explanation



# 📈 Model Performance

Model	               MAE	        Type
Random Forest	   963.33 ⭐	    Ensemble
Linear Regression	1,064.52	 Statistical
XGBoost	           1,999.98	     Boosting
LSTM	      —	                     Deep Learning
Prophet    	—	                     Time Series

# Evaluated on 12-month synthetic dataset. Larger datasets improve accuracy.

# 📁 Project Structure

finance-ai/
├── backend/
│   ├── app/
│   │   ├── api/routes/       # REST endpoints
│   │   ├── core/             # Config, security
│   │   ├── db/               # Database session
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   └── ml/               # ML models + artifacts
│   ├── requirements.txt
│   └── runtime.txt
├── frontend/
│   ├── src/
│   │   ├── api/              # Axios client
│   │   ├── components/       # Reusable UI
│   │   ├── context/          # Auth context
│   │   ├── pages/            # Route pages
│   │   └── utils/            # Helpers
│   └── package.json
├── data/sample/              # Sample CSVs (test data)
├── notebooks/                # Jupyter notebooks
├── docs/                     # Documentation
└── README.md



#  🎓 Academic Context

Project Title: AI-Based Financial Statement Analysis and Cash Flow Prediction System Using Machine Learning and Explainable AI

 # Novel Contributions:

1. Financial Health Score — Unified 0–100 metric from 7 ratios

2. Multi-model forecasting — Comparative benchmark across 5 algorithms

3. Explainable AI for finance — SHAP + LIME + natural language

4. Dual anomaly detection — Isolation Forest + statistical Z-score

5. End-to-end platform — From raw CSV to PDF/Excel report

# 📄 License

MIT License — free to use for educational purposes.


# 👤 Author

ChandraMouli-->[25102D020020]
GitHub : @dogga777  [https://github.com/dogga777]
Live Demo: finsight-frontend-laxo.onrender.com

<div align="center">
Built with ❤️ for intelligent financial analytics

⭐ Star this repo if you found it useful!

</div> ```
