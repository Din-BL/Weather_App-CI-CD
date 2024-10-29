from flask import Flask, render_template, request, redirect, url_for, send_file
from datetime import datetime
import requests
from dotenv import load_dotenv
import os
import json
import logging
import boto3
from prometheus_client import Counter, generate_latest, REGISTRY

app = Flask(__name__)

# Load environment variables
load_dotenv()
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')

dynamodb = boto3.client(
    'dynamodb',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.FileHandler("weather_app.log"),
                              logging.StreamHandler()])

# Prometheus metrics
REQUEST_COUNT = Counter('flask_app_request_count',
                        'Total number of requests to this Flask app', ['method', 'endpoint'])
CITY_LOOKUP_COUNT = Counter(
    'city_lookup_count', 'Total number of times each city has been looked at', ['city'])


@app.before_request
def before_request():
    REQUEST_COUNT.labels(request.method, request.path).inc()
    app.logger.info(f"Received {request.method} request for {request.path}")


@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY)


def remove_commas(input_string):
    return input_string.replace(',', '')


def convert_date_to_day(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    day_of_week = date_obj.strftime('%a')
    return day_of_week

# Helper function to save search query data to a JSON file


def save_search_to_file(location, data):
    # Create a dictionary for the data you want to store
    search_data = {
        "city": location,
        "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "weather": data  # Store the full weather data dictionary for flexibility
    }

    # Create a file name based on the city and current timestamp
    file_name = f"{location}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    file_path = os.path.join('history', file_name)

    # Ensure the directory exists
    os.makedirs('history', exist_ok=True)

    # Write the data to the JSON file
    with open(file_path, 'w') as f:
        json.dump(search_data, f, indent=4)

    app.logger.info(f'Search data saved to {file_path}')

    # Return the file name
    return file_name


@app.route('/')
def index():
    app.logger.debug('Rendering index page')
    bg_color = os.getenv('BG_COLOR', '#ffffff')
    return render_template('index.html', weather_data=[], file_name=None, bg_color=bg_color)


def current_Data(data):
    first_two_items = data[:2]
    merged_dict = {}
    for item in first_two_items:
        merged_dict.update(item)
    merged_dict.pop('data_conditions', None)
    return merged_dict


def pushed_to_DB(data):
    item = current_Data(data)
    dynamodb_item = {
        "City": {"S": item.get("data_address")},
        "Date": {"S": item.get("datetime")},
        "Tempmax": {"N": str(item.get("data_tempmax"))},
        "Temperature": {"N": str(item.get("temp"))},
        "Humidity": {"N": str(item.get("humidity"))},
        "Windspeed": {"N": str(item.get("windspeed"))},
        "Sunset": {"S": item.get("sunset")},
        "Conditions": {"S": item.get("conditions")}
    }

    try:
        app.logger.info("Pushing data to DynamoDB")
        dynamodb.put_item(
            TableName='WeatherData',
            Item=dynamodb_item
        )
        app.logger.info("Data pushed to DynamoDB successfully")
    except Exception as e:
        app.logger.error(f"Error pushing data to DynamoDB: {e}")


@app.route('/weather', methods=['POST'])
def weather():
    location = request.form.get('location')
    if not location:
        app.logger.warning('No location provided in request')
        return redirect(url_for('error'))
    key = os.getenv('WEATHER_KEY')
    if not key:
        app.logger.error('No API key found in environment variables')
        return redirect(url_for('error'))

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/next7days?unitGroup=metric&key={key}&contentType=json"
    app.logger.debug(f'Requesting weather data from {url}')

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        app.logger.info(f'Weather data retrieved for {location}')
    except requests.RequestException as e:
        app.logger.error(f"Request failed: {e}")
        return redirect(url_for('error'))
    except ValueError as e:
        app.logger.error(f"JSON decode failed: {e}")
        return redirect(url_for('error'))

    CITY_LOOKUP_COUNT.labels(city=location).inc()

    data_list = data.get('days')
    if not data_list:
        app.logger.warning(f'No weather data found for {location}')
        return redirect(url_for('error'))

    # Save search query to file and get the file name
    file_name = save_search_to_file(location, data)

    current_day = {
        "data_address": remove_commas(data.get('resolvedAddress')),
        "data_conditions": data_list[0]["conditions"],
        "data_tempmax": data_list[0]["tempmax"],
    }
    days_list = []
    for day in data_list:
        new_day = {
            "datetime": convert_date_to_day(day["datetime"]),
            "temp": day["temp"],
            "humidity": day["humidity"],
            "windspeed": day["windspeed"],
            "sunset": day["sunset"],
            "conditions": day["conditions"],
        }
        days_list.append(new_day)
    days_list.insert(0, current_day)

    bg_color = os.getenv('BG_COLOR', '#ffffff')

    return render_template('index.html', weather_data=days_list, file_name=file_name, bg_color=bg_color)


@app.route('/push_to_db', methods=['POST'])
def push_to_db():
    data = request.get_json()
    pushed_to_DB(data)
    return {'status': 'success'}, 200


@app.route('/error')
def error():
    app.logger.debug('Rendering error page')
    return render_template('error.html')

# Route to handle file download


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join('history', filename)

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        app.logger.error(f"File {filename} not found")
        return redirect(url_for('error'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
