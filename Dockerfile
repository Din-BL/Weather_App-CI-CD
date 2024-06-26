FROM python:3.12.3

WORKDIR /weather_app

RUN pip install --upgrade pip

RUN pip install flask requests python-dotenv

COPY weather_app /weather_app

CMD ["python", "app.py"]
