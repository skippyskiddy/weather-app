# Required modules
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import requests
import pytz

# Create a new Flask web server application
app = Flask(__name__)
# Enabling Cross Origin Resource Sharing for the server 
# to allow other servers to access the API
CORS(app, origins=["http://localhost:5173"])

# Defining a route for the '/weather' URL, for GET requests
@app.route('/weather', methods=['GET'])
def get_weather_for_location():
    # API keys for the OpenCageData and OpenWeatherMap services
    # Please fill in your own API keys here 
    opencage_api_key = 'insert-your-opencagedata-api-key-here'
    openweathermap_api_key = 'insert-your-openweathermap-api-key-here'

    # Extracts the 'location' parameter from the GET request
    location = request.args.get('location')

    try: # basic error handling
        # making a request to the OpenCageData API to get the lat and lon for the location
        response = requests.get(f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={opencage_api_key}")
        data = response.json()

        # Checking if the API call was successful
        if response.status_code != 200:
            return jsonify({'error': f"An error occurred with the OpenCageData API: {data['status']['message']}"}), response.status_code

        # Checking if the location exists in the OpenCageData API response
        if 'results' not in data or len(data['results']) == 0:
            return jsonify({'error': 'Location not found'}), 404

        # Extracting the latitude and longitude
        lat, lon = data['results'][0]['geometry']['lat'], data['results'][0]['geometry']['lng']

        # Making a request to the OpenWeatherMap API to get the weather for the location
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={openweathermap_api_key}")
        weather_data = response.json()

        # Checking if the API call was successful
        if response.status_code != 200:
            return jsonify({'error': 'An error occurred with the OpenWeatherMap API'}), response.status_code

        # Extracting and converting the temperature from Kelvin (from openweathermap) to Celsius
        temp_celsius = weather_data['main']['temp'] - 273.15
        # Extracting the general weather condition and the more specific description
        condition = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        # Extracting the timezone offset from UTC
        get_timezone_offset = weather_data['timezone']

        # Converting the timezone offset from seconds to hours and then to minutes
        timezone_offset_hours = get_timezone_offset / 3600
        timezone_offset_minutes = timezone_offset_hours * 60

        # Getting the current UTC time using pytz
        utc_time = datetime.now(pytz.utc)
        # Adjusting the UTC time for the timezone offset to get the local time
        local_time = utc_time.astimezone(pytz.FixedOffset(timezone_offset_minutes))
        # Formatting the local time
        formatted_local_time = local_time.strftime('%H:%M %p')

        # Returning the weather data as a JSON response
        return jsonify({
            'location': location,
            'local_time': formatted_local_time,
            'temperature': f"{temp_celsius:.1f}°C",
            'condition': condition,
            'description': description
        })
    except Exception as e:
        # If an error occurred, returns a 500 status code and a JSON with the error message
        return jsonify({'error': 'An error occurred while processing your request'}), 500

# Runs the server in debug mode as its not in prod 
if __name__ == "__main__":
    app.run(debug=True)
