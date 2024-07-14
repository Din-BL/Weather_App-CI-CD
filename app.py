from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import requests
from dotenv import load_dotenv
import os
import json
import subprocess

app = Flask(__name__)


def remove_commas(input_string):
    return input_string.replace(',', '')


def convert_date_to_day(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    day_of_week = date_obj.strftime('%a')
    return day_of_week


@app.route('/')
def index():
    # Pass an empty list as default weather_data
    return render_template('index.html', weather_data=[])


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
    item_json = json.dumps(dynamodb_item)
    command = [
        "aws", "dynamodb", "put-item",
        "--table-name", "WeatherData",
        "--item", item_json
    ]
    subprocess.run(command, capture_output=True, text=True)


@app.route('/weather', methods=['POST'])
def weather():
    location = request.form.get('location')
    if not location:
        return redirect(url_for('error'))
    load_dotenv()
    key = os.getenv('WEATHER_KEY')
    if not key:
        return redirect(url_for('error'))
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{
        location}/next7days?unitGroup=metric&key={key}&contentType=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        app.logger.error(f"Request failed: {e}")
        return redirect(url_for('error'))
    except ValueError as e:
        app.logger.error(f"JSON decode failed: {e}")
        return redirect(url_for('error'))
    data_list = data.get('days')
    if not data_list:
        return redirect(url_for('error'))
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
    pushed_to_DB(days_list)
    return render_template('index.html', weather_data=days_list)


@app.route('/push_to_db', methods=['POST'])
def push_to_db():
    data = request.get_json()
    pushed_to_DB(data)
    return {'status': 'success'}, 200


@app.route('/error')
def error():
    return render_template('error.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
