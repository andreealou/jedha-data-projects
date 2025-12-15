# Project 2 – Collection, Storage & Management of Data: KAYAK

## Objective

**What’s the best destination for your next holidays?**  
This project aims to identify the top holiday destinations in France based on **weather forecasts** and **hotel availability**.  
The goal is to collect, store, and organize this data using **AWS cloud services** and provide a clean dataset for further analysis.

---

## Context

The data collected comes from two main sources:

- **Weather API** (OpenWeather): to obtain 5-day weather forecasts for all French cities.
- **Booking.com Scraping**: to retrieve hotel data (name, score, description, coordinates, URL).

The final dataset combines these two sources to recommend destinations with both **good weather** and **attractive accommodation options**.

---

## Project Steps

### 1. Data Collection
- **Part 1:** GPS coordinates and city list creation.  
- **Part 2:** Weather data collected for the next 5 days via API calls.  
- **Part 3:** Web scraping of hotels using `Scrapy`, retrieving name, description, score, and location.

### 2. Data Lake (AWS S3)
- All CSV files were uploaded to **Amazon S3**, serving as a **data lake** for raw and enriched data.
- Two files were stored:
  - `Destinations_infos.csv` → Hotels information.
  - `moyenne_meteo_5jours.csv` → Weather forecasts.

### 3. Data Warehouse (AWS RDS)
- A **PostgreSQL** database was created using **AWS RDS**.
- Both datasets were extracted from S3 and loaded into RDS tables using **SQLAlchemy** and **Pandas**.

### 4. Data Visualization
- Several **interactive maps** were built with `Plotly Express`:
  - Average temperatures in France for the next 5 days.
  - Top 5 destinations with the best weather.
  - Hotel locations in the top destinations.

---

## Key Learnings

- Using **APIs** to collect real-time weather data.
- Implementing **web scraping** with Scrapy, handling anti-bot issues and dynamic pages.
- Managing cloud storage with **AWS S3**.
- Building and connecting to a **PostgreSQL** database on **AWS RDS**.
- Visualizing geospatial data with **Plotly Express**.

---

## Tech Stack

| Category | Tools / Libraries |
|-----------|-------------------|
| Language | Python |
| Data Collection | Scrapy, Requests, OpenWeather API |
| Data Processing | Pandas, NumPy |
| Cloud Services | AWS S3 (Data Lake), AWS RDS (PostgreSQL) |
| Database | SQLAlchemy, psycopg2 |
| Visualization | Plotly Express, Mapbox |
| Environment | Jupyter Notebook, VS Code |

---

## Results

- **Top 5 destinations** in France with the best weather forecast.  
- **List of hotels** available in these destinations (with score and location).  
- **Data stored in S3** as a data lake.  
- **Structured database in RDS** accessible for further analysis.

---

## Deliverables

- `Kayak.ipynb` → Complete pipeline notebook.  
- AWS S3 and RDS screenshots in the PDF Presentation

