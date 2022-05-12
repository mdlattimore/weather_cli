import requests
import datetime
import json
from app_id import app_id

def day_conversion(unix_time):
    local_unix_time = unix_time + data["timezone_offset"]
    day = datetime.datetime.utcfromtimestamp(local_unix_time).strftime('%A')
    return day

def date_conversion(unix_time):
    local_unix_time = unix_time + data["timezone_offset"]
    date = datetime.datetime.utcfromtimestamp(local_unix_time).strftime('%m-%d-%Y')
    return date

def time_conversion(unix_time):
    local_unix_time = unix_time + data["timezone_offset"]
    _time = datetime.datetime.utcfromtimestamp(local_unix_time).strftime('%I:%M %p')
    
    return _time

location = {
    "Matthews": {"lat": "35.116832866" , "lon": "-80.709830494", "offset": -4}
}


locale = input("Input city: ")

lat = location[locale.capitalize()]["lat"]
lon = location[locale.capitalize()]["lon"]

params = {"lat": lat, "lon": lon, "units": "imperial", "exclude": "minutely,hourly", "appid": app_id}

url = "https://api.openweathermap.org/data/2.5/onecall"

response = requests.get(url, params=params)

data = response.json()

print(json.dumps(data, indent=4))

# Current Conditions
def display_current():
    current_day = day_conversion(data["current"]["dt"])
    current_date = date_conversion(data["current"]["dt"])
    local_time = time_conversion(data["current"]["dt"])
    sunrise = time_conversion(data["current"]["sunrise"])
    sunset = time_conversion(data["current"]["sunset"])
    temp = data["current"]["temp"]
    feels_like = data["current"]["feels_like"]
    pressure = data["current"]["pressure"]
    humidity = data["current"]["humidity"]
    dew_point = data["current"]["dew_point"]
    weather_main = data["current"]["weather"][0]["main"]
    weather_description = data["current"]["weather"][0]["description"]

    # Display Current Info
    print()
    print("Current Weather")
    print()
    print(f"Today: {current_day}")
    print(f"Date: {current_date}")
    print(f"Current time: {local_time}")
    print(f"Sunrise: {sunrise}")
    print(f"Sunset: {sunset}")
    print(f"Current temp: {temp} degrees")
    print(f"Feels like: {feels_like} degrees")
    print(f"Barometric pressure: {pressure}")
    print(f"Humidity: {humidity}%")
    print(f"Dew point: {dew_point} degrees")
    print(f"Currently: {weather_main}, {weather_description}")
    print()
    print()

# Forecast
def display_forecast():
    print("Eight Day Forecast")
    print()
    for day in data["daily"]:
        f_day = day_conversion(day["dt"])
        date = date_conversion(day["dt"])
        sunrise = time_conversion(day["sunrise"])
        sunset = time_conversion(day["sunset"])
        high_temp = day["temp"]["max"]
        low_temp = day["temp"]["min"]
        humidity = day["humidity"]
        dew_point = day["humidity"]
        weather_main = day["weather"][0]["main"]
        weather_description = day["weather"][0]["description"]
        print(f_day)
        print(f"Date: {date}")
        print(f"Sunrise: {sunrise}")
        print(f"Sunset: {sunset}")
        print(f"High: {high_temp} degrees")
        print(f"Low: {low_temp} degrees")
        print(f"Humidity: {humidity}%")
        print(f"Dew Point: {dew_point} degrees")
        print(f"Weather: {weather_main}, {weather_description}")
        print()
        print("*********")
        print()

display_current()
display_forecast()




