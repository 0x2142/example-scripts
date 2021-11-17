import json
import logging

import requests
from webex_bot.models.command import Command

log = logging.getLogger(__name__)

# Get a free account at openweathermap.org &
# insert API key here:
OPENWEATHER_KEY = ""


class WeatherByZIP(Command):
    def __init__(self):
        # Define custom command info here
        # command_keyword = what chat keyword will trigger this command to execute
        # help_message = what message is returned when user sends 'help' message
        # card = optionally send an AdaptiveCard response
        super().__init__(
            command_keyword="weather",
            help_message="Get current weather conditions by ZIP code.",
            card=None,
        )

    def execute(self, message, attachment_actions):
        # By default, command keyword will be stripped out before being passed to execute function
        # For example, If user sends "weather 12345", then message variable will be " 12345"
        # Need to strip the additional whitespace around the input:
        zip_code = message.strip()

        # Define our URL, with desired parameters: ZIP code, units, and API Key
        url = "https://api.openweathermap.org/data/2.5/weather?"
        url += f"zip={zip_code}&units=imperial&appid={OPENWEATHER_KEY}"

        # Query weather
        response = requests.get(url)
        weather = response.json()

        # Pull out desired info
        city = weather["name"]
        conditions = weather["weather"][0]["description"]
        temperature = weather["main"]["temp"]
        humidity = weather["main"]["humidity"]
        wind = weather["wind"]["speed"]

        # Format message that will be sent back to the user
        response_message = (
            f"In {city}, it's currently {temperature}F with {conditions}. "
        )
        response_message += f"Wind speed is {wind}mph. Humidity is {humidity}%"

        # Message returned will be sent back to the user by bot
        return response_message
