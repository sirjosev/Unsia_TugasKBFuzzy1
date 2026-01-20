FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories to ensure permissions
RUN mkdir -p src data

COPY . .

# Expose port 7860 for Hugging Face Spaces
EXPOSE 7860

HEALTHCHECK CMD curl --fail http://localhost:7860/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=7860", "--server.address=0.0.0.0"]
