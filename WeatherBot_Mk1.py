import requests
#import asyncio
import discord
from datetime import datetime
#import schedule
from discord.ext import commands # tasks

#Constants
BOT_TOKEN = "MTE4NzQ2MDc4Mjg3OTk0ODg3MQ.GrQr7o.Q7CQfc6r229dgVUd9mnqCKSiz3S0cLSDEqXGGk"
#Use for sunny and clear
SUNNY_ICON = ":sunny:"
#Use for cloudy and overcast
CLOUDY_ICON = ":cloud:"
#partly cloudy
PARTLY_ICON = ":partly_sunny:"
#use for Moderate rain/light rain/heavy rain
RAIN_ICON = ":cloud_rain:"
#use for stormy
STORM_ICON = ":cloud_lighting:"
#use for snowy
SNOW_ICON = ":cloud_snow:"
#Use for patchy rain
PATCHY_ICON = ":white_sun_rain_cloud:"
SKULL = ":skull:"
HOT_FACE = ':hot_face:'
SWEAT_SMILE = ':sweat:'
BLUSH = ':blush:'
GRIN = ':grin:'
GRIMACE = ':grimacing:'
COLD_FACE = ':cold_face:'
ICE = ':ice_cube:'


#APIs
CURRENT_API_URL = "http://api.weatherapi.com/v1/current.json"
FORECAST_API_URL = "http://api.weatherapi.com/v1/forecast.json"
WEATHER_API_KEY = "d5eebc64a2b045f997f122138242604"  

CHANNEL_ID = 1187480788262977636

#Global Variables
city = "Clemson, SC"

#FUNCTIONS
 
#Function fecthes the weather data from WeatherAPI.com api
def get_weather(api_key, city):
    try:
        querystring = {"key": api_key, "q": city}
        response = requests.get(CURRENT_API_URL, params = querystring)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error fetching weather data:", e)
        return None

def get_forecast(api_key, days):
    try:
        querystring = {"key": api_key, "q": city, "days": days}
        response = requests.get(FORECAST_API_URL, params=querystring)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error fetching weather data:", e)
        return None
        
        
#Set the command prefix for bot commands
bot = commands.Bot(command_prefix = "w/", intents = discord.Intents.all())

#creates readable weather information based on selected cit
def display_current_weather():
    api_key = WEATHER_API_KEY
    
    weather_data = get_weather(api_key, city)

    # Extract relevant information from the response
    location = weather_data['location']['name']
    country = weather_data['location']['country']
    temperature = weather_data['current']['temp_f']
    condition = weather_data['current']['condition']['text']

    # Display weather information
    loc_str = (f"Weather in {location}, {country}:\n")
    temp_str = (f"Temperature: {add_Ticons(temperature)}°F\n")
    cond_str = (f"Condition: {add_Cicons(condition)}")
    concat_str = loc_str + temp_str + cond_str
    
    return concat_str
def add_Cicons(condition):
    if condition == "Sunny" or condition == "Clear":
        condition += f' {SUNNY_ICON}'
    elif condition == "Partly Cloudy":
        condition += f' {PARTLY_ICON}'
    elif condition == "Light rain" or condition == "Moderate rain" or condition == "Heavy rain":
        condition += f' {RAIN_ICON}'
    elif condition == "Snowy":
        condition += f' {SNOW_ICON}'
    elif condition == "Stormy":
        condition += f' {STORM_ICON}'
    elif condition == "Patchy rain nearby":
        condition += f' {PATCHY_ICON}'
    elif condition == "Cloudy" or condition == "Overcast":
        condition += f' {CLOUDY_ICON}'

    cond_message = f'{condition}'
    print(cond_message)
    return cond_message

def add_Ticons(temp):
    float(temp)
    if temp >= 110:
        icon = SKULL
    elif temp >= 90:
        icon = HOT_FACE
    elif temp >= 80:
        icon = SWEAT_SMILE
    elif temp >= 70:
        icon = BLUSH
    elif temp >= 60:
        icon = GRIN
    elif temp >= 40:
        icon = GRIMACE
    elif temp >= -20:
        icon = COLD_FACE
    elif temp >= -130:
        icon = ICE
    
    temp_str = f'{temp}°F {icon}'
    return temp_str

#function generates readable forecast data
def display_3d_forecast():
    days = 3
    api_key = WEATHER_API_KEY
    forecast_data = get_forecast(api_key, days)
    
    
    if forecast_data:
        forecast_days = forecast_data['forecast']['forecastday']
        forecast_message = f'{days}-Day Forecast for {city}:\n'
        for day in forecast_days:
            date = day['date']
            condition = day['day']['condition']['text']
            max_temp = day['day']['maxtemp_f']
            min_temp = day['day']['mintemp_f']
            print('before')
            forecast_message += f'{date}:\n\t{add_Cicons(condition)}\n\tHigh: {add_Ticons(max_temp)}\n\tLow: {add_Ticons(min_temp)}\n'
        
        return forecast_message
    else:
        return "Failed to fetch forecast data."
            
            
"""
#Function for checking the time and triggering the hourly update
async def check_hour():
    await bot.wait_until_ready()
    while not bot.is_closed():
            currTime = datetime.now()
            if currTime.minute == 0 and currTime.second == 0:
                await hourly_update()
            await asyncio.sleep(60)

#Send the hourly update
def hourly_update():
    currTime = datetime.now()
    formattedTime = currTime.strftime("%H:%M")
    print(formattedTime)

"""

#BOT COMMANDS/EVENTS

#schedule.every().hour.do(hourly_update)

@bot.event
async def on_ready():
    print("WeatherBot is Ready")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Its time for the Weather with me weather boy!")
    await channel.send("Here is the current weather:\n" + display_current_weather())
    
    #Send weather upadate each hour
    #bot.loop.create_task(check_hour())

#Command for changing the city
@bot.command()
async def setcity(ctx, new_city: str):
    global city
    city = new_city
    await ctx.channel.send(f"City is now set to {city}:\n" + display_current_weather())

#Command for requesting a n day forecast
@bot.command()
async def forecast(ctx):
    days = 3
    #if days > 14 or days < 1:
    #   await ctx.channel.send("Please enter a number 1-14.\n")
    #else:
    await ctx.channel.send(f"Here is your {days} day forecast:\n" + display_3d_forecast())

        
    

bot.run(BOT_TOKEN)
