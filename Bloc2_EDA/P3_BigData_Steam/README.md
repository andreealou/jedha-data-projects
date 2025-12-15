# P3 – Big Data Pipeline: Steam / Spark / Redshift

## Project Objective
The goal of this project is to build a complete Big Data architecture to collect, store, and analyze a large volume of data from the **Steam** platform, in order to identify key trends in the video game market (pricing, developers, publishers, popularity, etc.).

---

## Project Architecture

### 1. **Data Collection and Storage**
- Raw dataset available on a public S3 bucket:  
  `s3://full-stack-bigdata-datasets/Big_Data/Project_Steam/steam_game_output.json`
- Format: **JSON**, containing main information for each game:
  - `appid`
  - `name`
  - `release_date`
  - `developer`
  - `publisher`
  - `genres`
  - `price`

---

### 2. **Data Ingestion into Redshift**
Data from S3 is loaded into **Amazon Redshift** using the `COPY` command:

```sql
CREATE TABLE steam_games (
    appid INT,
    name VARCHAR(500),
    release_date VARCHAR(50),
    developer VARCHAR(500),
    publisher VARCHAR(500),
    genres VARCHAR(500),
    price FLOAT
);

COPY steam_games
FROM 's3://full-stack-bigdata-datasets/Big_Data/Project_Steam/steam_game_output.json'
CREDENTIALS 'aws_access_key_id=XXX;aws_secret_access_key=YYY'
FORMAT AS JSON 'auto'
REGION 'eu-west-3';
```

This step structures the data into a scalable, queryable data warehouse.

---

### 3. **Processing and Analysis with Databricks (PySpark)**
Once the data is available in Redshift, the connection is established from **Databricks** using the JDBC connector:

```python
REDSHIFT_USER = "my_user"
REDSHIFT_PASSWORD = "my_password"
REDSHIFT_FULL_PATH = "jdbc:postgresql://redshift-cluster-1.xxxxx.eu-west-3.redshift.amazonaws.com:5439/dev"
REDSHIFT_TABLE = "steam_games"

connection_props = {
    "user": REDSHIFT_USER,
    "password": REDSHIFT_PASSWORD,
    "driver": "org.postgresql.Driver"
}

df = spark.read.jdbc(
    url=REDSHIFT_FULL_PATH,
    table=REDSHIFT_TABLE,
    properties=connection_props
)

df.show(5)
```

---

### 4. **Data Cleaning and Exploration**
In Databricks, the data is transformed and analyzed using **PySpark**:

- Handling missing values and duplicates  
- Converting release dates to proper formats  
- Descriptive analysis:  
  - Number of games by developer/publisher  
  - Genre distribution  
  - Correlation between price and release date  
- Visualizations with Spark and Matplotlib/Pandas to explore market trends  

---

## Technical Skills Demonstrated
- **Cloud & Big Data:**
  - AWS S3 (data storage)
  - AWS Redshift (data warehouse)
  - Databricks (distributed processing)
- **Languages:**
  - SQL  
  - Python / PySpark  
- **Additional Concepts:**
  - ETL data pipeline design  
  - JDBC connections  
  - JSON schema handling  
  - Scalable data analysis  

---

## Key Results
- Complete Big Data pipeline implementation (S3 → Redshift → Databricks)  
- Successful JDBC connection between Redshift and Databricks  
- Cleaned and structured dataset for analysis  
- Insights and visualizations on pricing and genre distribution in the Steam market  

---

## Project Structure
```
P3_BigData_Steam/
│
├── steam_load_redshift.sql      # SQL script (CREATE TABLE + COPY)
├── databricks_connection.ipynb  # PySpark notebook (Redshift connection)
├── steam_analysis.ipynb         # Analysis & visualization notebook
└── README.md                    # This file
```
