# Credit Card Customer Churn Analytics Platform📊

A full-stack analytics application that helps a bank identify customers at risk of churning, understand what drives attrition, and estimate the business impact of retention efforts.

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)

![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)
![Scikit--Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?logo=scikitlearn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-1A1A1A?logo=xgboost&logoColor=white)
![SHAP](https://img.shields.io/badge/SHAP-FF6B6B?logo=python&logoColor=white)

![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?logo=tailwindcss&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3D4F71?logo=plotly&logoColor=white)

![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

**Dataset:** [Credit Card Customers (Kaggle)](https://www.kaggle.com/datasets/sakshigoyal7/credit-card-customers)

## Deliverables

| Module                | What it does                                                                        | Key outputs                                                                                                                                                |
| --------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **EDA Dashboard**     | Visual breakdown of demographics, engagement, product usage, and churn distribution | **10,127** customers · **16.07%** churn rate · segment-level churn by income, card type, and education                                                     |
| **Model Performance** | XGBoost evaluation with recall-weighted scoring and SHAP explainability             | F2 **0.919** · ROC AUC **0.993** · avg precision **0.968** · threshold **0.478**                                                                           |
| **Customer Explorer** | Browse customer records from PostgreSQL with churn filters                          | 10,127 seeded records · filter by attrited vs existing customers                                                                                           |
| **Churn Prediction**  | Real-time scoring with risk band and explainable drivers                            | Churn probability · High / Medium / Low risk band · top **SHAP drivers** (transaction count, transaction amount, revolving balance, avg transaction value) |
| **Business Impact**   | Retention ROI simulation under configurable save-rate assumptions                   | **1,354** high-risk customers · **$609,300** revenue at risk · **$152,325** estimated saved at **25%** intervention rate ($450/customer/year)              |

**Top SHAP churn drivers:** transaction count (12 mo) → transaction amount → revolving balance → avg transaction value → transaction count change (Q4 vs Q1).

**High-risk proxy (business impact):** inactive ≥ 3 months · contacted ≥ 3 times · below-median transaction count.

## Run the App

```bash
docker compose up -d
```

Open http://127.0.0.1:5173 · Stop with `docker compose down`

**First-time setup:**

```bash
docker compose up -d --build
docker compose run --rm backend python scripts/seed_database.py --input ../data/raw/BankChurners.csv
docker compose run --rm backend python scripts/train_model.py --input ../data/raw/BankChurners.csv --artifacts ../data/artifacts
```
