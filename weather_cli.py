import requests
import datetime
import json
from app_id import app_id
import argparse
import os
import pydoc

# TODO Convert current info to pydoc

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

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
    print(f"Barometric pressure: {pressure} millibars")
    print(f"Humidity: {humidity}%")
    print(f"Dew point: {dew_point} degrees")
    print(f"Currently: {weather_main}, {weather_description}")
    print()
    print()

# Forecast
def display_forecast():
    forecast = "\nEight Day Forecast\n\n"  # Assemble formatted dispaly into string so we can pass to pydoc.pager()
    for day in data["daily"]:
        f_day = day_conversion(day["dt"])  # use f_day ("forecast day") so as not to shadow "day" in for loop.
        date = date_conversion(day["dt"])
        sunrise = time_conversion(day["sunrise"])
        sunset = time_conversion(day["sunset"])
        high_temp = day["temp"]["max"]
        low_temp = day["temp"]["min"]
        humidity = day["humidity"]
        dew_point = day["humidity"]
        weather_main = day["weather"][0]["main"]
        weather_description = day["weather"][0]["description"]
        forecast += (f_day) + "\n"
        forecast += f"Date: {date}\n"
        forecast += f"Sunrise: {sunrise}\n"
        forecast += f"Sunset: {sunset}\n"
        forecast += f"High: {high_temp} degrees\n"
        forecast += f"Low: {low_temp} degrees\n"
        forecast += f"Humidity: {humidity}%\n"
        forecast += f"Dew Point: {dew_point} degrees\n"
        forecast += f"Weather: {weather_main}, {weather_description}\n\n"
    return forecast

location = {
    "Matthews": {"lat": "35.116832866" , "lon": "-80.709830494", "offset": -4}
}


parser = argparse.ArgumentParser()
parser.add_argument("city")     
parser.add_argument("-f", "--forecast",
                    help="Eight Day Forecast",
                    action="store_true")
args = parser.parse_args()

locale = args.city
lat = location[locale.capitalize()]["lat"]
lon = location[locale.capitalize()]["lon"]

params = {"lat": lat, "lon": lon, "units": "imperial", "exclude": "minutely,hourly", "appid": app_id}

url = "https://api.openweathermap.org/data/2.5/onecall"

response = requests.get(url, params=params)

data = response.json()

if args.forecast:
    clear()
    display = display_forecast()
    pydoc.pager(display)
else:
    clear()
    display_current()



# print(json.dumps(data, indent=4))






