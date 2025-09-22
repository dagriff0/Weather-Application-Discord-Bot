import requests

#RAPID_URL = "https://weatherapi-com.p.rapidapi.com/current.json"
#RAPID_API_KEY = "KEY"
#RAPID_API_HOST = "weatherapi-com.p.rapidapi.com"

WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"
WEATHER_API_KEY = "KEY GOES HERE"  # Replace this with your RapidAPI key

def get_weather(api_key, city):
    try:
        querystring = {"key": api_key, "q": city}
        response = requests.get(WEATHER_API_URL, params = querystring)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error fetching weather data:", e)
        return None


def main():
    api_key = WEATHER_API_KEY
    city = "29630"
    weather_data = get_weather(api_key, city)

    # Extract relevant information from the response
    location = weather_data['location']['name']
    country = weather_data['location']['country']
    temperature = weather_data['current']['temp_f']
    condition = weather_data['current']['condition']['text']

    # Display weather information
    print(f"Weather in {location}, {country}:")
    print(f"Temperature: {temperature}°C")
    print(f"Condition: {condition}")

if __name__ == "__main__":
    main()
