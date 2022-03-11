# Simple Webex Chatbot

This repo contains example code for creating a Webex chatbot. The bot has the ability to query OpenWeatherMap.org APIs and return the current weather conditions. 

This example leverages the [webex_bot](https://github.com/fbradyirl/webex_bot) module to quickly & easily build a Webex bot. webex_bot uses websockets to create a direct connection to the Webex Cloud, therefore avoiding some of the complexities required with using webhooks.

To use this code:
- Install webex_bot: `pip install webex_bot` 
- Open `weather.py` and input your OpenWeather API key
- Set your Webex bot API key as an environment variable: `export WEBEX_TOKEN=<apikey>`
- Run `python bot.py`
- Open Webex & chat with your bot!

A Webex API key can be created by signing up for a free developer account at developer.webex.com

## Additional Details

- [Blog Post](https://0x2142.com/how-to-building-a-basic-webex-chatbot/)
- [YouTube Video](https://www.youtube.com/watch?v=yZQjoe5XUYE)
