FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install pytest

COPY app.py .env /app/

COPY templates/ templates/
COPY static/ static/

CMD ["python", "app.py"]





