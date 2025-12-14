# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy API code and model file into the image
COPY api_app.py .
COPY getaround_pricing_model.joblib .

# Expose the API port expected by Hugging Face
EXPOSE 7860

# Command to start FastAPI with Uvicorn
CMD ["uvicorn", "api_app:app", "--host", "0.0.0.0", "--port", "7860"]

