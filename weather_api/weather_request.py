import requests 
from datetime import datetime
import pytz
# using the built in python request library


def get_lat_lon(api_key, location):
    response = requests.get(f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={api_key}")
    data = response.json()
    return data['results'][0]['geometry']['lat'], data['results'][0]['geometry']['lng']

def get_weather(api_key, lat, lon):
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}")
    
    # print(response.json())
    # line to print the full api response
    # can help debug issues with OpenWeatherMap API
    return response.json()

def get_local_time(get_timezone_offset):
    # Convert the offset to hours
    timezone_offset_hours = get_timezone_offset / 3600
    timezone_offset_minutes = timezone_offset_hours * 60

    # Get the current UTC time
    utc_time = datetime.now(pytz.utc)
    # Shift the current UTC time by the timezone offset to get the local time
    local_time = utc_time.astimezone(pytz.FixedOffset(timezone_offset_minutes))
    formatted_local_time = local_time.strftime('%H:%M %p')

    return formatted_local_time


def main():
    # API keys
    opencage_api_key = 'insert-your-opencagedata-api-key-here'
    openweathermap_api_key = 'insert-your-openweathermap-api-key-here'

    location = input("Enter your location name (City or Country): ")
    #print(location)

    try:
        # Convert the location to latitude and longitude
        lat, lon = get_lat_lon(opencage_api_key, location)

        # Get the current weather data for the given coordinates
        weather_data = get_weather(openweathermap_api_key, lat, lon)

        # Extract the temperature and convert it from Kelvin to Celsius
        temp_celsius = weather_data['main']['temp'] - 273.15

        # Extract the general weather condition and the more specific description
        condition = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']

        # Extract the timezone offset from UTC in seconds
        get_timezone_offset = weather_data['timezone']
        formatted_local_time = get_local_time(get_timezone_offset)

        print(f"Current weather in {location} at {formatted_local_time}\n:{temp_celsius:.1f}°C, {condition} ({description})")

    except Exception as e:
        print(f"An error occurred: {e}")


    
if __name__ == "__main__":
    main()