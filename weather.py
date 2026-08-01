import requests
import argparse

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Icy fog",
    51: "Light drizzle",
    61: "Light rain",
    71: "Light snow",
    80: "Rain showers",
    95: "Thunderstorm"
}

def get_coordinates(city):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    response = requests.get(geo_url)

    data = response.json()
    if not data.get("results"):
        print("City not found.Please check the city name and try again.")
        return None
    else:
        latitude = data['results'][0]['latitude']
        longitude = data['results'][0]['longitude']
        return latitude, longitude

def get_weather(city):
    location_data = get_coordinates(city)
    if location_data is None:
        return None

    latitude, longitude = location_data
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,windspeed_10m,weathercode"
    response = requests.get(weather_url)
    return response.json()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get current weather information for a specified city.")
    parser.add_argument("--city", type=str, help="Name of the city to get weather information for.")

    args = parser.parse_args()
    city = args.city
    weather_data = get_weather(city)
    
    if weather_data:
        weathercode = weather_data['current']['weathercode']
        weather_description = WEATHER_CODES.get(weathercode, "Unknown")
        print(f"Weather in {city}:")
        print(f"Temperature: {weather_data['current']['temperature_2m']}°C")
        print(f"Weather: {weather_description}")
        print(f"Humidity: {weather_data['current']['relative_humidity_2m']}%")
        print(f"Wind Speed: {weather_data['current']['windspeed_10m']} m/s")