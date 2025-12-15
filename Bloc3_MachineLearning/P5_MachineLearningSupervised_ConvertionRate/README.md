# P5 – Supervised Machine Learning:  Conversion Rate Prediction


## Objective
The goal of this supervised machine learning project was to **predict whether a user will convert (subscribe to a newsletter)** based on behavioral and demographic features.  
The final model must be evaluated using the **F1-score**, as required by the challenge.

---

## Dataset
Two CSV files were provided:
- `conversion_data_train.csv` → training dataset with labels  
- `conversion_data_test.csv` → test dataset without labels  

### Main features
| Feature | Description |
|----------|--------------|
| `country` | User country |
| `age` | User age |
| `new_user` | 1 = new visitor, 0 = returning |
| `source` | Traffic source (Ads, SEO, Direct) |
| `total_pages_visited` | Number of pages viewed before leaving the site |
| `converted` | Target variable (1 = converted, 0 = not converted) |

---

## Data Analysis Summary
- The dataset is **strongly imbalanced**: only a small percentage of users convert.  
- The variable **`total_pages_visited`** is by far the most predictive:  
  users visiting more than 10–15 pages have a much higher chance of converting.  
- Other variables (age, new_user, country, source) have weaker correlations.

---

## Preprocessing
- Handling categorical variables using **OneHotEncoder**  
- Scaling numeric features with **StandardScaler**  
- Stratified train/test split (`stratify=Y`) to preserve class balance  

---

## Models Tested
Several families of supervised models were compared:

| Model | Method | F1 (train) | F1 (test) | Comments |
|--------|---------|------------|-----------|-----------|
| Logistic Regression | Baseline | 0.7620 | 0.7675 | Solid baseline |
| Ridge (L2) | Regularized | 0.7620 | 0.7675 | Similar to baseline |
| Lasso (L1) | Regularized | 0.7619 | **0.7683** | ✅ Best model |
| Elastic Net | Regularized | 0.7619 | 0.7683 | Similar to Lasso |
| Decision Tree | Non-linear | 0.7688 | 0.7563 | Overfitting |
| Random Forest | Bagging | 0.7737 | 0.7601 | Slightly better generalization |
| XGBoost | Gradient Boosting | 0.7626 | 0.7641 | Stable but not superior |
| AdaBoost | Adaptive Boosting | 0.7578 | 0.7673 | Competitive alternative |

---

## Feature Engineering
Two rounds of feature engineering were performed:

### V12 – General Feature Engineering
- `log_total_pages`: logarithmic transformation  
- `pages_x_newuser`: interaction between engagement and novelty  
- `age_bin`: age categories  
- `is_ads`: binary indicator for ad source  
- `country_simplified`: rare countries grouped as “Other”  

➡️ No significant F1-score improvement (dataset too simple).

### V13 – Targeted Feature Engineering on `total_pages_visited`
- `pages_bin`: user engagement categories (low, medium, high, power)  
- `is_power_user`: binary feature for users visiting >15 pages  
- `is_low_engagement`: binary feature for users visiting <3 pages  

➡️ Useful for interpretability and for potential improvement with non-linear models.

---

## Best Model
**Lasso Logistic Regression (penalty='l1', C=10, solver='saga')**

| Metric | Train | Test |
|---------|-------|------|
| **F1-score** | 0.7619 | **0.7676** |
| **Confusion Matrix (test)** | [[54882, 198], [569, 1267]] |

✅ Balanced model with no overfitting and very interpretable coefficients.

---

## Key Insights
- The **number of pages visited** is the dominant factor for predicting conversion.  
- Users coming from **ads** and **returning visitors** convert more often.  
- Age and country have minimal influence.

---

## Business Recommendations
1. **Encourage users to visit more pages**  
   - Improve UX and site navigation.  
   - Add recommended content and internal links.  

2. **Optimize acquisition sources**  
   - Prioritize the most profitable channels (Ads vs Direct).  

3. **Improve onboarding for new users**  
   - New visitors convert less → guide them with tutorials, popups, or incentives.

---

## Conclusion
The **Lasso Logistic Regression** provided the best trade-off between simplicity, performance, and interpretability.  
Boosting methods (AdaBoost, XGBoost) achieved similar F1-scores but at a higher computational cost.  
Further gains could come from more **behavioral features** (time spent, click types, session duration) rather than new model architectures.

---

## Tech Stack
- Python 3.12  
- Pandas, NumPy, Scikit-learn, XGBoost  
- Jupyter Notebook  
- Visualization: Matplotlib, Seaborn

---

## Versions Overview
| Version | Focus | Notebook |
|----------|--------|-----------|
| V7 | Logistic Regression, Ridge, Lasso, ElasticNet | ✅ Main baseline |
| V8 | Decision Tree | Overfitting test |
| V9 | Random Forest | Bagging |
| V10 | XGBoost | Gradient Boosting |
| V11 | AdaBoost | Adaptive Boosting |
| V12 | Global Feature Engineering | Broad feature tests |
| V13 | Targeted Feature Engineering | Focus on `total_pages_visited` |

