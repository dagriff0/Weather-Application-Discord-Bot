import requests

RAPID_URL = "https://weatherapi-com.p.rapidapi.com/current.json"
RAPID_API_KEY = "48f568b40bmsh578205faacc6f62p1d11a0jsn109f2a5ba371"  # Replace this with your RapidAPI key
RAPID_API_HOST = "weatherapi-com.p.rapidapi.com"

def get_weather(api_key, city):
    querystring = {"q": city}
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': RAPID_API_HOST
    }
    response = requests.request("GET", RAPID_URL, headers=headers, params=querystring)
    data = response.json()
    return data

def main():
    api_key = RAPID_API_KEY
    city = "Clemson"
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
