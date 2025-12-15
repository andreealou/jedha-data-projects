# P8 – Deployment: Getaround Delay Analysis & ML Model Deployment

## Jedha – Advanced Data Science Bootcamp

This project reproduces Getaround’s internal 2017 analysis regarding late returns, operational conflicts, and optimal minimum delay thresholds. It also includes a pricing prediction API (FastAPI) and a Streamlit dashboard.

---

# Project Overview

Getaround enables peer-to-peer car rentals through two check-in flows:

- **Mobile** (owner meets driver)  
- **Connect** (remote unlock)

Late returns can disrupt operations when two rentals are scheduled too closely.

Main questions:

- How frequent are late returns?  
- How many rentals are impacted?  
- What minimum buffer reduces conflicts?  
- Differences between Mobile vs Connect?  
- Can we predict rental prices using ML?

---

# Repository Structure

```
.
├── get_around_delay_analysis.xlsx
├── get_around_pricing_project.csv
├── getaround_delay_analysis.ipynb
├── api_app.py
├── gradient_boosting.joblib
├── preprocessor.joblib
├── streamlit_app.py
└── README.md
```

---

# 1. Delay Analysis (EDA)

## 1.1 Key Metrics

| Metric | Value |
|-------|-------|
| Total rentals | 21,310 |
| Chain rentals (<12h gap) | 1,476 |
| Actual conflicts | 172 |
| Conflict rate (overall) | 0.81% |
| Conflict rate (chain rentals) | 11.65% |

Insight: although conflicts are rare overall, **1 in 9 tightly scheduled rentals** results in an operational conflict.

---

## 1.2 Check-in Type Distribution

- Mobile ~80%  
- Connect ~20%

Conflicts mainly stem from Mobile, the dominant flow.

---

## 1.3 Checkout Outcomes

Returns can be:

- Early  
- On time  
- Late  

Early returns are surprisingly common.

---

## 1.4 Delay Distribution

- **Short delays (±2h):** most returns fall between −60 and +120 minutes  
- **Medium delays (2–24h):** many around 2–3 hours  
- **Extreme delays (>24h):** rare but disruptive  

---

# 2. Conflict Detection

A conflict occurs when:

```
previous_delay > available_gap
```

Steps:

1. Join each rental with delay of previous rental  
2. Keep rentals with <12h gap  
3. Flag conflicts where previous delay exceeds the gap  

Result → **172 operational conflicts**, mostly when gaps < 60 min.

---

# 3. Minimum Gap Threshold Simulation

Business rule tested:

> A car cannot be re-booked unless at least X minutes separate two rentals.

| Threshold | Conflicts Resolved | Total | % |
|----------|--------------------|-------|----|
| 0 min | 0 | 172 | 0% |
| 15 min | 42 | 172 | 24% |
| 30 min | 60 | 172 | 35% |
| 45 min | 73 | 172 | 42% |
| 60 min | 86 | 172 | 50% |
| 90 min | 112 | 172 | 65% |
| 120 min | 124 | 172 | 72% |

Recommendation: adopt a **60–90 min** buffer.

---

# 4. Streamlit Dashboard

Includes:

- Check-in distribution  
- Delay histograms  
- Early-return behaviour  
- Gap structure  
- Conflict detection  
- Threshold simulation  
- Recommendations  

Run locally:

```bash
streamlit run streamlit_app.py
```

---

# 5. Machine Learning Model (Pricing)

Gradient Boosting model using:

- model_key  
- mileage  
- engine_power  
- fuel, paint_color, car_type  
- gps, AC, Connect, regulator  
- winter_tires  
- private_parking_available  

Artifacts:

```
gradient_boosting.joblib
preprocessor.joblib
```

---

# 6. FastAPI – /predict Endpoint

Run API:

```bash
uvicorn api_app:app --reload
```

Example request:

```json
{
  "model_key": "Citroen",
  "mileage": 88000,
  "engine_power": 110,
  "fuel": "diesel",
  "paint_color": "black",
  "car_type": "sedan",
  "private_parking_available": true,
  "has_gps": false,
  "has_air_conditioning": true,
  "automatic_car": false,
  "has_getaround_connect": true,
  "has_speed_regulator": true,
  "winter_tires": false
}
```

Example response:

```json
{
  "rental_price_per_day": 42.75
}
```

Docs → `/docs` and `/redoc`.

---

# 7. Deployment

- API deployed on Hugging Face Spaces  
- Dashboard deployable on Streamlit Cloud or Hugging Face  
- Uses FastAPI, Uvicorn, Streamlit  

---

# 8. Installation & Setup

```bash
git clone https://github.com/andreea73/getaround_project.git
cd getaround_project
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
uvicorn api_app:app --reload
```

---

# 9. Business Recommendations

- Adopt **60–90 min** minimum delay buffer  
- Prioritise Mobile rentals  
- Encourage early returns  
- Improve UX to avoid 0-minute gaps  

---

# Conclusion

This project includes:

- Exploratory analysis  
- Operational risk modelling  
- Pricing ML model  
- FastAPI deployment  
- Streamlit dashboard  

It provides actionable insights directly aligned with Getaround’s operational needs.
