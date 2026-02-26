# 🌾 Crop Recommendation & Agricultural Advisory System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python" />
  <img src="https://img.shields.io/badge/Flask-REST%20API-black?style=flat-square&logo=flask" />
  <img src="https://img.shields.io/badge/ML-Random%20Forest%20%7C%20SVM%20%7C%20LR-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/Domain-Precision%20Agriculture-green?style=flat-square" />
</p>

> A full-stack agricultural advisory platform that integrates crop recommendation, disease detection, irrigation planning, market insights, and weather forecasting — powered by an ML backend and served via a Flask REST API.

---

## 📋 Table of Contents

- [Research Question](#-research-question)
- [Modules](#-modules)
- [Dataset & Features](#-dataset--features)
- [Methodology](#-methodology)
- [Results](#-results)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [How to Run](#-how-to-run)
- [Limitations](#-limitations)
- [References](#-references)

---

## ❓ Research Question

> *Can a multi-variate soil and climate model reliably recommend optimal crops and advisory actions for diverse regional agricultural conditions — and can this be delivered as a usable, real-time decision support system?*

Modern precision agriculture demands more than yield maximization — it requires risk-aware recommendations that account for soil biochemistry, climate variability, and resource constraints simultaneously. This project investigates whether classical ML classifiers can serve this role effectively without deep learning overhead.

---

## 🧩 Modules

This platform is not a single model — it's a multi-module advisory system:

| Module | Template | Purpose |
|---|---|---|
| 🌱 Crop Recommendation | `crop.html` | Recommends optimal crop based on soil & climate inputs |
| 🦠 Disease Detection | `disease.html` | Identifies crop diseases from symptoms or images |
| 💧 Irrigation Planning | `irrigation.html` | Estimates irrigation requirements based on conditions |
| 📈 Market Insights | `market.html` | Provides crop price trends and market signals |
| 🌦️ Weather Advisory | `weather.html` | Integrates real-time weather for farming decisions |
| 🤖 AI Chatbot | `chatbot.html` | Conversational interface for agricultural Q&A |

---

## 📊 Dataset & Features

**Crop Recommendation Dataset**
- **Samples:** 2,200 labeled crop records
- **Source:** [Kaggle — Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)
- **Target Classes:** 22 crop types

**Input Features (7 parameters):**

| Feature | Unit | Description |
|---|---|---|
| Nitrogen (N) | mg/kg | Soil nitrogen content |
| Phosphorus (P) | mg/kg | Soil phosphorus content |
| Potassium (K) | mg/kg | Soil potassium content |
| Temperature | °C | Ambient temperature |
| Humidity | % | Relative humidity |
| Soil pH | — | Soil acidity/alkalinity (0–14) |
| Rainfall | mm | Annual rainfall |

---

## ⚙️ Methodology

### Phase 1 — Preprocessing
- StandardScaler applied to normalise all 7 features to zero mean and unit variance
- No missing values in the dataset; verified via null checks
- 80/20 stratified train-test split to preserve class balance across 22 crop types

### Phase 2 — Model Benchmarking
Three classifiers benchmarked under identical conditions:

| Model | Why Chosen |
|---|---|
| Random Forest | Handles feature interactions well; provides feature importance |
| SVM (RBF Kernel) | Effective in moderate-dimensional spaces with clear margins |
| Logistic Regression | Baseline; provides calibrated probability outputs |

### Phase 3 — Interpretability
Feature importance extracted from Random Forest to identify which soil/climate parameters drive each crop recommendation — enabling explainable outputs rather than black-box predictions.

---

## 📈 Results

| Model | Accuracy | Notes |
|---|---|---|
| Random Forest | **99.55%** | Best model — saved for inference |
| SVM (RBF) | 98.41% | Strong performance, slower inference |
| Logistic Regression | 97.27% | Baseline — fast and interpretable |

> All models trained with 80/20 stratified split, `random_state=42`, on 2,200 patient samples across 22 crop classes.

---

## 📁 Project Structure

```
agriculture-advisory/
│
├── main.py                        ← Flask app entry point & API routes
│
├── templates/
│   ├── index2.html                ← Landing page
│   ├── crop.html                  ← Crop recommendation interface
│   ├── disease.html               ← Disease detection interface
│   ├── irrigation.html            ← Irrigation planning interface
│   ├── market.html                ← Market insights dashboard
│   ├── weather.html               ← Weather advisory interface
│   └── chatbot.html               ← AI chatbot interface
│
├── model/                         ← Trained model files (.pkl)
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Backend | Python 3.9+, Flask (REST API) |
| ML Engine | Scikit-learn (Random Forest, SVM, Logistic Regression) |
| Data Processing | Pandas, NumPy |
| Frontend | HTML5, CSS3, JavaScript |

---

## 🚀 How to Run

```bash
# 1. Clone the repository
git clone https://github.com/Lakshminarayan566/agriculture-advisory
cd agriculture-advisory

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Flask app
python main.py

# 4. Open in browser
# → http://localhost:5000
```

**Expected output:** Flask development server starts on port 5000 with all advisory modules accessible via the navigation menu.

---

## ⚠️ Limitations

- Crop recommendation model trained on a single publicly available dataset — regional soil variation not fully captured
- Disease detection module accuracy depends heavily on input quality (symptom description clarity)
- Market insights are not connected to a live price feed — static or manually updated data only
- Weather module relies on a third-party API; accuracy is bound by that API's coverage

---

## 📚 References

1. Crop Recommendation Dataset — [Kaggle, Atharva Ingle](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)
2. Breiman, L. (2001). Random Forests. *Machine Learning*, 45, 5–32.
3. Flask Documentation — https://flask.palletsprojects.com/

---

<p align="center">
  Soil · Climate · ML · Real-Time Advisory · 22 Crop Classes
</p>
