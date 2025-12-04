# P4 – Supervised Machine Learning: Walmart Sales Forecasting

## 🎯 Project Overview
The objective of this project is to **predict weekly sales for Walmart stores** using historical data and explanatory features such as temperature, fuel price, CPI, and unemployment.  
By analyzing past performance and external factors, this model aims to help decision-makers **anticipate future trends** and understand what drives store performance.

---

## 📂 Dataset
**Source:** Provided by Jedha Bootcamp  
**File:** `Walmart_Store_sales.csv`

**Main columns:**
- `Store` → Store number (categorical)  
- `Date` → Week date (time series)  
- `Weekly_Sales` → Weekly sales amount (target)  
- `Holiday_Flag` → Indicates if the week includes a holiday  
- `Temperature` → Average temperature that week  
- `Fuel_Price` → Fuel price in the region  
- `CPI` → Consumer Price Index  
- `Unemployment` → Unemployment rate  

---

## 🧹 Data Preprocessing
1. **Date parsing** and extraction of new features:
   - `Year`, `Month`, and `Week`
2. **Outlier removal** using the 3-sigma rule:  
   \[
   [\bar{X} - 3\sigma, \bar{X} + 3\sigma]
   \]  
   Applied to `Temperature`, `Fuel_Price`, `CPI`, and `Unemployment`.
3. **Missing value imputation:**
   - Numeric → Median  
   - Categorical → Most frequent value  
4. **Feature scaling** using `StandardScaler`.  
5. **One-hot encoding** of categorical variables (`Store`, `Holiday_Flag`).

---

## 🤖 Machine Learning Models
Three supervised regression models were trained and compared:

| Model | MAE | RMSE | R² |
|--------|-------|-------|-------|
| Linear Regression | **104,239** | **130,067** | **0.9638** |
| Ridge Regression | 175,770 | 239,715 | 0.8769 |
| Lasso Regression | **104,240** | **130,071** | **0.9638** |

✅ **Lasso Regression** achieved the same performance as Linear Regression while performing **feature selection** by reducing irrelevant coefficients to zero.

---

## ⚙️ Regularization Optimization
Hyperparameter tuning was tested using **GridSearchCV** on Ridge and Lasso models.  
However, optimized models yielded lower R² scores (≈0.79–0.89), meaning manual tuning provided better performance.  

> This suggests that overly strong regularization can lead to underfitting for this dataset.

---

## 📈 Model Evaluation
Metrics used:
- **MAE (Mean Absolute Error)** – average deviation between predictions and actual values  
- **RMSE (Root Mean Squared Error)** – penalizes large errors  
- **R² (Coefficient of Determination)** – proportion of variance explained by the model  

Additional visualizations:
- Actual vs Predicted scatterplots  
- Weekly trends and store-level sales evolution  
- Correlation heatmaps and outlier inspection  

---

## 🧠 Key Insights
- Sales patterns vary seasonally, with clear peaks around holiday weeks.  
- Lasso’s feature selection highlights that not all stores or weeks contribute equally to predictive accuracy.  
- CPI and Unemployment show limited direct correlation with weekly sales, while Store ID and time-based features dominate.

---

## 🪄 Tech Stack
- **Language:** Python 3  
- **Libraries:** pandas, numpy, scikit-learn, matplotlib, seaborn  
- **Environment:** Jupyter Notebook / VS Code  
- **ML Workflow:** scikit-learn Pipeline + GridSearchCV  


