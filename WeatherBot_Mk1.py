import requests
import asyncio
import discord
from datetime import datetime
import schedule
from discord.ext import commands, tasks

#Constants
BOT_TOKEN = "MTE4NzQ2MDc4Mjg3OTk0ODg3MQ.GrQr7o.Q7CQfc6r229dgVUd9mnqCKSiz3S0cLSDEqXGGk"
RAPID_URL = "https://weatherapi-com.p.rapidapi.com/current.json"
RAPID_API_KEY = "48f568b40bmsh578205faacc6f62p1d11a0jsn109f2a5ba371"  # Replace this with your RapidAPI key
RAPID_API_HOST = "weatherapi-com.p.rapidapi.com"
CHANNEL_ID = 1187480788262977636

#Global Variables
city = "Clemson, SC"
    
#Function fecthes the weather data from WeatherAPI.com api
def get_weather(api_key, city):
    querystring = {"q": city}
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': RAPID_API_HOST
    }
    response = requests.request("GET", RAPID_URL, headers=headers, params=querystring)
    data = response.json()
    return data

#creates readable weather information based on selected cit
def display_weather():
    api_key = RAPID_API_KEY
    
    weather_data = get_weather(api_key, city)

    # Extract relevant information from the response
    location = weather_data['location']['name']
    country = weather_data['location']['country']
    temperature = weather_data['current']['temp_f']
    condition = weather_data['current']['condition']['text']

    # Display weather information
    loc_str = (f"Weather in {location}, {country}:\n")
    temp_str = (f"Temperature: {temperature}°F\n")
    cond_str = (f"Condition: {condition}")
    concat_str = loc_str + temp_str + cond_str
    
    return concat_str

bot = commands.Bot(command_prefix = "w/", intents = discord.Intents.all())

def hourly_update():
    currTime = datetime.now()
    formattedTime = currTime.strftime("%H:%M")
    print(formattedTime)
    
    
async def check_hour():
    await bot.wait_until_ready()
    while not bot.is_closed():
            currTime = datetime.now()
            if currTime.minute == 0 and currTime.second == 0:
                await hourly_update()
            await asyncio.sleep(60)

#schedule.every().hour.do(hourly_update)

@bot.event
async def on_ready():
    print("WeatherBot is Ready")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Its time for the Weather with me weather boy!")
    await channel.send("Here is the current weather:\n" + display_weather())
    
    #Send weather upadate each hour
    bot.loop.create_task(check_hour())

@bot.command()
async def setcity(ctx, new_city: str):
    global city
    city = new_city
    await ctx.channel.send(f"City is now set to {city}:\n" + display_weather())
    
    

bot.run(BOT_TOKEN)
