import requests
import asyncio
import discord
from datetime import datetime
import schedule
from discord.ext import commands, tasks

BOT_TOKEN = "TOKEN HERE"

#WEATHER ICONS
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

#TEMPERATURE ICONS
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
WEATHER_API_KEY = "KEY HERE"  

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
    feels_like = weather_data['current']['feelslike_f']

    # Display weather information
    loc_str = (f"Weather in {location}, {country}:\n")
    temp_str = (f"Temperature: {add_Ticons(temperature)}\n")
    cond_str = (f"Condition: {add_Cicons(condition)}\n")
    f_like_str = (f"Feels Like: {add_Ticons(feels_like)}\n")
    concat_str = loc_str + temp_str + f_like_str + cond_str
    
    return concat_str
#Icons for the current weather conditions
def add_Cicons(condition):
    
    temp_lower = condition.lower()
    
    if condition == "Sunny" or condition == "Clear":
        condition += f' {SUNNY_ICON}'
    elif "partly cloudy" in temp_lower:
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

#Icons for temperature
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

#function creates 3 day forecast message
def display_3d_forecast():
    days = 3
    api_key = WEATHER_API_KEY
    forecast_data = get_forecast(api_key, days)
    
    
    if forecast_data:
        forecast_days = forecast_data['forecast']['forecastday']
        forecast_message = f'{days}-Day Forecast for {city}:\n'
        for day in forecast_days:
            date = day['date']
            # Convert date string to a datetime object
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            # Get the day of the week
            day_of_week = date_obj.strftime('%A')
            condition = day['day']['condition']['text']
            max_temp = day['day']['maxtemp_f']
            min_temp = day['day']['mintemp_f']
            forecast_message += f'{day_of_week}:\n\t{add_Cicons(condition)}\n\tHigh: {add_Ticons(max_temp)}\n\tLow: {add_Ticons(min_temp)}\n'
        
        return forecast_message
    else:
        return "Failed to fetch forecast data."
                        
# Function to send weather updates to the channel
async def send_weather_update():
    channel = bot.get_channel(CHANNEL_ID)
    current_hour = datetime.now().strftime("%-I %p")
    weather_update = display_current_weather()
    await channel.send(f"Here is your {current_hour} O'clock weather update:\n" + weather_update)

# Schedule the weather update every hour
def schedule_weather_updates():
    schedule.every().hour.at(":00").do(lambda: asyncio.run_coroutine_threadsafe(send_weather_update(), bot.loop))

#BOT COMMANDS/EVENTS
#On Join
@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(f"Hello {guild.name}! Thank you for inviting me!")
            break
    await channel.send("""Please set a default channel for me! You can do this by using the command "w/setchannel" in the channel you want.""")

#On Ready
@bot.event
async def on_ready():
    print("WeatherBot is Ready!")
    """
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Its time for the Weather with me WeatherBot!")
    await channel.send("Here is the current weather:\n" + display_current_weather())
    schedule_weather_updates()
    check_schedule.start()
    """
    
#Help Command
@bot.command()
async def botinfo(ctx):
    info_message = ("""I am a Weather Bot here to keep you up to date on the current weather. I give hourly updates and can give you forecasts for the coming days. You can even change which city I am set to.
            Here are my current available commands:
                    \tw/botinfo - displays bot information and commands
                    \tw/setchannel - sets the default channel
                    \tw/now - displays the current weather
                    \tw/forecast - displays a 3 day forecast
                    \tw/setcity [city] - changes the current city and immediately displays the weather\n
                    Powered by WeatherAPI.com and Developed by Davidillionaire Inc.""")
    await ctx.channel.send(info_message)

@bot.command()
async def setchannel(ctx):
    global CHANNEL_ID
    CHANNEL_ID = ctx.channel
    await ctx.channel.send("Awesome! From now on I will use this channel for Hourly updates and routine messages!")
    await ctx.channel.send("To view my commands and Info please use the w/botinfo command!")
    
#Command for displaying current weather
@bot.command()
async def now(ctx):
    await ctx.channel.send("Here is the current weather:\n" + display_current_weather())

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

#checks the time every minute
@tasks.loop(seconds=60)
async def check_schedule():
    schedule.run_pending()
        
    

bot.run(BOT_TOKEN)
