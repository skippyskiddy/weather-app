from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import requests
import pytz

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

@app.route('/weather', methods=['GET'])
def get_weather_for_location():
    opencage_api_key = 'insert-your-opencagedata-api-key-here'
    openweathermap_api_key = 'insert-your-openweathermap-api-key-here'

    location = request.args.get('location')

    try:
        response = requests.get(f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={opencage_api_key}")
        data = response.json()

        if response.status_code != 200:
            return jsonify({'error': f"An error occurred with the OpenCageData API: {data['status']['message']}"}), response.status_code

        if 'results' not in data or len(data['results']) == 0:
            return jsonify({'error': 'Location not found'}), 404

        lat, lon = data['results'][0]['geometry']['lat'], data['results'][0]['geometry']['lng']

        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={openweathermap_api_key}")
        weather_data = response.json()

        if response.status_code != 200:
            return jsonify({'error': 'An error occurred with the OpenWeatherMap API'}), response.status_code

        temp_celsius = weather_data['main']['temp'] - 273.15
        condition = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        get_timezone_offset = weather_data['timezone']

        timezone_offset_hours = get_timezone_offset / 3600
        timezone_offset_minutes = timezone_offset_hours * 60
        utc_time = datetime.now(pytz.utc)
        local_time = utc_time.astimezone(pytz.FixedOffset(timezone_offset_minutes))
        formatted_local_time = local_time.strftime('%H:%M %p')

        return jsonify({
            'location': location,
            'local_time': formatted_local_time,
            'temperature': f"{temp_celsius:.1f}°C",
            'condition': condition,
            'description': description
        })
    except Exception as e:
        return jsonify({'error': 'An error occurred while processing your request'}), 500

if __name__ == "__main__":
    app.run(debug=True)
