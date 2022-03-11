import json
import logging

import requests
from webex_bot.models.command import Command
from webex_bot.models.response import Response
from adaptivecardbuilder import *
from datetime import datetime


log = logging.getLogger(__name__)

# Get a free account at openweathermap.org &
# insert API key here:
OPENWEATHER_KEY = ""

with open("./input-card.json", "r") as card:
    INPUT_CARD = json.load(card)

class WeatherByZIP(Command):
    def __init__(self):
        # Define custom command info here
        # command_keyword = what chat keyword will trigger this command to execute
        # help_message = what message is returned when user sends 'help' message
        # card = optionally send an AdaptiveCard response
        super().__init__(
            command_keyword="weather",
            help_message="Get current weather conditions by ZIP code.",
            card=INPUT_CARD,
        )

    def execute(self, message, attachment_actions, activity):
        # By default, all incoming input will come from adaptive card submission
        # Will pull 'zip_code' from incoming attachment_actions dictionary
        zip_code = attachment_actions.inputs['zip_code']

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
        low_temp = weather["main"]["temp_min"]
        high_temp = weather["main"]["temp_max"] 
        humidity = weather["main"]["humidity"]
        pressure = weather["main"]["pressure"]
        wind = weather["wind"]["speed"]
        sunrise = datetime.fromtimestamp(weather["sys"]["sunrise"]).strftime(f"%I:%M%p")
        sunset = datetime.fromtimestamp(weather["sys"]["sunset"]).strftime(f"%I:%M%p")

        # Build adaptive card
        # For more info around structure, check adaptivecardbuilder project readme
        card = AdaptiveCard()
        card.add(
            [
                TextBlock(text=f"Weather for {city}", size="Medium", weight="Bolder"),
                ColumnSet(),
                    Column(width="stretch"),
                        FactSet(),
                            Fact(title="Temp", value=f"{temperature}F"),
                            Fact(title="Conditions", value=f"{conditions}"),
                            Fact(title="Wind", value=f"{wind} mph"),
                            "<",
                        "<",
                    Column(width="stretch"),
                        FactSet(),
                        Fact(title="High", value=f"{high_temp}F"),
                        Fact(title="Low", value=f"{low_temp}F"),
                        "^",
                ActionSet(),
                    ActionShowCard(title="More Details"),
                        ColumnSet(),
                            Column(width="stretch"),
                                FactSet(),
                                    Fact(title="Humidity", value=f"{humidity}%"),
                                    Fact(title="Pressure", value=f"{pressure} hPa"),
                                    "<",
                                "<",
                            Column(width="stretch"),
                                FactSet(),
                                    Fact(title="Sunrise", value=f"{sunrise}"),
                                    Fact(title="Sunset", value=f"{sunset}"),
            ]
        )
        # Convert card data to JSON
        card_data = json.loads(asyncio.run(card.to_json()))

        # Add necessary headers to attach card for response
        card_payload = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": card_data,
        }

        # Build card response
        response = Response()
        # Fallback text
        response.text = "Test Card"
        # Attachments being sent to user
        response.attachments = card_payload

        return response
