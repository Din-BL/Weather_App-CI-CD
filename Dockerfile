FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install pytest

COPY app.py .env . 
COPY templates/ templates/
COPY static/ static/

RUN mkdir -p /home/ec2-user/production/weather_app_logs

CMD ["python", "app.py"]











