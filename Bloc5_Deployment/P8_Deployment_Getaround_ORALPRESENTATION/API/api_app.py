from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import numpy as np
import joblib

# -----------------------------------------------------
# FastAPI initialization
# -----------------------------------------------------

app = FastAPI(
    title="Getaround Pricing API",
    description="Endpoints for pricing prediction & documentation.",
    version="1.0",
    docs_url="/swagger",        # Swagger auto ⇢ /swagger
    redoc_url="/redocumentation"  # ReDoc auto ⇢ /redocumentation
)

# ------------------------------------------------------
# Model loading
# ------------------------------------------------------

MODEL_PATH = "getaround_pricing_model.joblib"
model = joblib.load(MODEL_PATH)


# ------------------------------------------------------
# Request schema
# ------------------------------------------------------

class PredictionInput(BaseModel):
    input: list


# ------------------------------------------------------
# /predict endpoint
# ------------------------------------------------------

@app.post("/predict")
def predict_price(payload: PredictionInput):
    """
    POST /predict
    Body:
    {
        "input": [[...], [...]]
    }
    """
    data = np.array(payload.input)
    preds = model.predict(data)
    preds_list = preds.tolist()
    return {"prediction": preds_list}



# ------------------------------------------------------
# /docs : Custom HTML documentation required by the project
# ------------------------------------------------------

@app.get("/docs", response_class=HTMLResponse)
def custom_docs():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Getaround Pricing API – Documentation</title>
        <meta charset="utf-8" />
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 40px auto;
                line-height: 1.6;
            }
            h1 {
                color: #B01AA7;
            }
            h2 {
                margin-top: 30px;
            }
            code {
                background-color: #f4f4f4;
                padding: 2px 4px;
                border-radius: 3px;
                font-size: 0.95em;
            }
            pre {
                background-color: #f4f4f4;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
                font-size: 0.9em;
            }
            .method {
                display: inline-block;
                padding: 3px 7px;
                border-radius: 4px;
                background-color: #B01AA7;
                color: white;
                font-weight: bold;
                font-size: 0.8em;
            }
            .section {
                margin-bottom: 25px;
            }
        </style>
    </head>
    <body>
        <h1>Getaround Pricing API – Documentation</h1>
        <p>
            This page explains how to use the pricing prediction API hosted on Hugging Face.
            The model predicts the <b>daily rental price</b> based on 55 input features
            (car characteristics and encoded categorical variables).
        </p>
        <div class="section">
            <h2>📌 API URLs</h2>
            <ul>
                <li><b>Space (Hugging Face):</b>
                    <code>https://huggingface.co/spaces/Andreea73/getaround_princing_API_Docker</code>
                </li>
                <li><b>Healthcheck (GET /):</b>
                    <code>https://andreea73-getaround-princing-api-docker.hf.space/</code>
                </li>
                <li><b>Prediction endpoint (POST /predict):</b>
                    <code>https://andreea73-getaround-princing-api-docker.hf.space/predict</code>
                </li>
                <li><b>Custom documentation (this page – GET /docs):</b>
                    <code>https://andreea73-getaround-princing-api-docker.hf.space/docs</code>
                </li>
                <li><b>Swagger UI (interactive docs):</b>
                    <code>https://andreea73-getaround-princing-api-docker.hf.space/swagger</code>
                </li>
            </ul>
        </div>
        <div class="section">
            <h2><span class="method">POST</span> /predict</h2>
            <p>
                Returns pricing predictions for one or multiple rentals.
                The body must contain a JSON object with a single key <code>"input"</code>,
                whose value is a list of rows. Each row is a list of <b>55 numeric features</b>.
            </p>
            <h3>Request body (JSON)</h3>
            <p>Example with one sample (55 features):</p>
            <pre>{
  "input": [[140411, 100, 1, 1, 0, 0, 1, 1, 1, 106,
             0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 1,
             0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0]]
}</pre>
            <h3>Response body (JSON)</h3>
            <p>The API returns a list of predictions, one per input row:</p>
            <pre>{
  "prediction": [108.87]
}</pre>
            <p>
                The value is the <b>predicted rental price per day</b> for each provided sample.
            </p>
        </div>
        <div class="section">
            <h2>🧪 Test the /predict endpoint online (Swagger)</h2>
            <ol>
                <li>Open <code>https://andreea73-getaround-princing-api-docker.hf.space/swagger</code></li>
                <li>Click on <b>POST /predict</b></li>
                <li>Click on <b>"Try it out"</b></li>
                <li>Paste the JSON body above and click <b>"Execute"</b></li>
            </ol>
        </div>
        <div class="section">
            <h2>💻 Test with curl (Terminal)</h2>
            <pre>curl -X POST "https://andreea73-getaround-princing-api-docker.hf.space/predict" \\
  -H "Content-Type: application/json" \\
  -d '{"input": [[140411,100,1,1,0,0,1,1,1,106,
                  0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                  0,0,1,
                  0,0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0]]}'</pre>
        </div>
        <div class="section">
    <h2>🐍 Test with Python</h2>
    <p>You can also call the API from a Python script, for example <code>test_api.py</code>:</p>
    <pre>import requests
url = "https://andreea73-getaround-princing-api-docker.hf.space/predict"
payload = {
    "input": [
        [
            140411, 100,
            1, 1, 0, 0, 1, 1, 1, 106,
            0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 1,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0
        ]
    ]
}
response = requests.post(url, json=payload)
print("Status code:", response.status_code)
print("Response JSON:", response.json())</pre>
    <p><b>In the Terminal, execute:</b></p>
    <pre>python test_api.py</pre>
    <p>This will print the predicted rental price returned by the API.</p>
</div>
        <p style="margin-top:40px;color:#666;font-size:0.9em;">
            © Getaround Pricing API – Demo project
        </p>
    </body>
    </html>
    """
    return html



# ------------------------------------------------------
# Optional health check
# ------------------------------------------------------

@app.get("/")
def health():
    return {"status": "ok", "message": "API running"}