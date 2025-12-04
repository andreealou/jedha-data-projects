# P6 – Unsupervised Machine Learning: Uber Pickup Clustering (NYC 2014–2015)

## 📌 Project Overview

This project analyzes **Uber pickup patterns in New York City** using **unsupervised learning techniques**. The goal is to identify **geographical hot zones**, understand how demand evolves **throughout the day**, and compare trends between the **2014 GPS-based dataset** and the **2015 zone-based dataset**.

We apply:
- **K-Means** → broad, centroid-based segmentation  
- **DBSCAN** → density-based clustering revealing natural pickup zones  
- **Geospatial visualization** (GeoPandas, Contextily, Plotly)  
- **Temporal analysis** → hourly animation of cluster activity  
- **2015 zone-level analysis** using official NYC Taxi Zones

---

## 📂 Datasets

### **2014 Uber GPS Datasets (April–September 2014)**
7 CSV files with fields:
- `Date/Time`
- `Lat`, `Lon`
- `Base`

→ Used for K-Means, DBSCAN, and geospatial clustering.

### **2015 Uber Dataset (January–June 2015)**
Single CSV:
- `Pickup_date`
- `Dispatching_base_num`
- `Affiliated_base_num`
- `locationID` (NYC taxi zone ID)

→ No coordinates, so used for **zone-level analysis**.

### **NYC Taxi Zone Shapefile**
Contains:
- `LocationID`
- `Borough`
- `Zone`
- Polygon geometry  

→ Used to map 2015 demand geographically.

---

## 🛠️ Preprocessing

After concatenating the 2014 files, we:
- Converted pickup timestamps to **datetime**
- Extracted features: `hour`, `day`, `month`, `weekday`, `is_weekend`
- Removed invalid coordinates
- Sampled subsets when needed for performance (DBSCAN & animations)

Full dataset:
4.53 million rows
9 engineered features


---

## 📊 Exploratory Data Analysis (EDA)

### Temporal Patterns
- Morning peak around **8–9 AM** (commuting hours)  
- Evening activity **4–7 PM**  
- Weekends shift toward nightlife and leisure districts  

### Geospatial Patterns
Heatmaps reveal:
- Strong activity in **Midtown** and **Downtown Manhattan**  
- Heavy airport activity (**JFK**, **LaGuardia**)  
- Growing demand in Brooklyn & Queens  

---

## 🟦 K-Means Clustering (Exploratory Step)

We first apply K-Means (`k=6`) to obtain a simple segmentation.

**Why K-Means?**
- Fast and intuitive baseline  
- Creates **six circular clusters** based on proximity to centroids  
- Helps visualize the **global distribution** of demand  

Main areas detected:
- Midtown  
- Downtown  
- Airports  
- Brooklyn hotspots  

---

## 🟩 DBSCAN – Density-Based Clustering (Main Model)

DBSCAN is the core model for discovering **organic hot zones**.

**Parameters:**
- `eps = 0.01`  
- `min_samples = 50`

**Strengths:**
- Finds clusters of arbitrary shape  
- Automatically detects the number of clusters  
- Ignores isolated noise points  

**Results:**
- **7 high-density clusters** detected  
- Correspond to real-world hotspots (Midtown, Downtown, JFK, LGA, Brooklyn)  
- **Silhouette Score ~ 0.23** (expected for geospatial DBSCAN)

DBSCAN provides a **realistic map** of mobility patterns across NYC.

---

## ⏱️ Temporal Animation (Plotly)

To explore **how each cluster evolves over 24 hours**, we:

1. Fit DBSCAN once on a large sample  
2. Assign each point its cluster  
3. Create a Plotly animation showing **hour-by-hour activity**

**Key observations:**
- Early morning → activity in residential zones  
- Midday → strong concentration in business districts  
- Evening → peaks in nightlife and airport areas  

The animation was exported as a **video** for Google Slides.

---

## 📍 Appendix – 2015 Pickup Analysis by Taxi Zone

Since the 2015 dataset lacks GPS coordinates, we used **NYC taxi zones** instead.

Steps:
1. Load 2015 CSV  
2. Load shapefile (`LocationID`, geometry)  
3. Count pickups per zone  
4. Plot a choropleth map  

**Findings:**
- Midtown remains the highest-demand zone  
- Airports are major demand hubs  
- Brooklyn & Queens show increased activity vs 2014  
- Confirms an **expansion of Uber usage** outside Manhattan

---

## 📈 Comparison 2014 vs 2015

- 2014: GPS precision → fine-grained DBSCAN clusters  
- 2015: Zone aggregation → macro-level validation  
- Consistent hotspots across years  
- Increasing decentralization of Uber demand  

---

## 💡 Final Insights & Recommendations

- Uber can optimize **driver positioning** based on hourly cluster patterns  
- Anticipate **surge pricing** at airports and nightlife zones  
- DBSCAN provides the most realistic segmentation for operational decisions  
- Future improvements:
  - Try **HDBSCAN** for multi-density clustering  
  - Demand forecasting with **Prophet**  
  - Build a real-time hotspot detector (streaming)

---

## ⚙️ Installation & Requirements

Python 3.10+ pandas numpy matplotlib seaborn geopandas contextily scikit-learn plotly