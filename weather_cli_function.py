import requests
import datetime
import json
from app_id import app_id
import argparse
import os
import pydoc
import sys
from rich.console import Console
from rich import print as rprint
from rich.text import Text
from rich.padding import Padding

# TODO Convert current info to pydoc
# TODO Format custom error messages with textwrap or format using """ """
# TODO Document functions

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


def location_api_call(location):
    params = {"q": location, "appid": app_id}
    url = "https://api.openweathermap.org/geo/1.0/direct"
    response = requests.get(url, params=params)
    data = response.json()
    city = data[0]["name"]
    state = data[0]["state"]
    lat = data[0]["lat"]
    lon = data[0]["lon"]
    return (city, state, lat, lon)


def forecast_api_call(lat, lon, app_id):
    params = {"lat": lat, "lon": lon, "units": "imperial", "exclude": "minutely,hourly", "appid": app_id}
    url = "https://api.openweathermap.org/data/2.5/onecall"
    response = requests.get(url, params=params)
    data = response.json()
    return data


def display_current(data, city, state):
    data = forecast_api_call(lat, lon, app_id)
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
    rprint(f"Current Weather for [bright_blue]{city}, {state}[/bright_blue]")
    print()
    rprint(f"Today: {current_day}")
    print(f"Date: {current_date}")
    print(f"Current time: {local_time}")
    rprint(f"Sunrise: {sunrise} :sunrise:")
    rprint(f"Sunset: {sunset} :sunset:")
    if temp >= 90:
        rprint(f"Current temp: {temp} degrees :hot_face:")
    else:
        rprint(f"Current temp: {temp} degrees")
    print(f"Feels like: {feels_like} degrees")
    print(f"Barometric pressure: {pressure} millibars")
    print(f"Humidity: {humidity}%")
    print(f"Dew point: {dew_point} degrees")
    if "clear" in weather_main.lower():
        rprint(f"Currently: {weather_main}, {weather_description} :sunglasses:")
    elif "clouds" in weather_main.lower():
        rprint(f"Currently: {weather_main}, {weather_description} :cloud:")
    else:
        rprint(f"Currently: {weather_main}, {weather_description}")

    print()
    print()


# Forecast
def display_forecast(data, city, state):
    forecast = f"\nEight Day Forecast for {city}, {state}\n\n"  # Assemble formatted dispaly into string so we can pass to pydoc.pager()
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

console = Console()

# Set up the CLI
parser = argparse.ArgumentParser(
                                description="A command line weather tool. The only required argument is city. See the help information on 'city' for syntax help. Without optional argument '-f', application displays current weather. When the '-f' is included, the application displays an 8 day forecast.",
                                epilog="The weather is here, wish you were beautiful. Wait! That's not right."
)
parser.add_argument("city",
                    help="You may search by entering only the name of the city to be searched. For cities whose name is more than one word, enclose the city name in quotation marks. For locations in the US, if you wish to search by city and state, you must enter the argument using the following sytanx {city},{state},us. Note the city, state, and country (US) are separated by commas with no spaces and the country code 'us' must be included. As before, multi-word entries must be enclosed in quotation marks. For locations outside the US, you can enter the argument {city},{country}.")     
parser.add_argument("-f", "--forecast",
                    help="Shows the eight day forecast for the location",
                    action="store_true")
                    
args = parser.parse_args()

error_msg = Text()
try:
    location_data = location_api_call(args.city)
except (IndexError, KeyError):
    print()
    error_msg.append("Your search failed. There are two likely explanations. The first is you've searched a location not recognized by the API that returns weather information. The second is you have incorrectly formatted the search argument. If you are adding a state to a search for a location in the United States, you must also include the US country code ('us') in the argument so that the search is in the format {city},{state},us (comma separated, no spaces). If you are searching cities composed of more than one word, you must enclose the city name in quotation marks. See help for more information.")
    rprint(Padding(error_msg,1))  # Error message put into Text() object then wrapped in Padding object to give one character padding around text.
    print()
    sys.exit()

city, state, lat, lon = (location_data)

if args.forecast:
    clear()
    data = forecast_api_call(lat, lon, app_id)
    display = display_forecast(data, city, state)
    pydoc.pager(display)
else:
    clear()
    data = forecast_api_call(lat, lon, app_id)
    display = display_current(data, city, state)
    

# Uncomment only for diagnostic purposes. Displays full results of forecast_api_call in json format
# print(json.dumps(data, indent=4))
# print(json.dumps(location_data, indent=4))






