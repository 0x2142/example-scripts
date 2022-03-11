# Webex Chatbot with Adaptive Cards

This repo builds upon the previous example in [this repo](https://github.com/0x2142/example-scripts/tree/master/simple-webex-chatbot). The bot has the ability to query OpenWeatherMap.org APIs and return the current weather conditions. In this iteration of the bot, we've added support for Adaptive Cards - to provide an easier way to input & display data.


To use this code:
- Install webex_bot: `pip install webex_bot` 
- Open `weather.py` and input your OpenWeather API key
- Set your Webex bot API key as an environment variable: `export WEBEX_TOKEN=<apikey>`
- Run `python bot.py`
- Open Webex & chat with your bot!

A Webex API key can be created by signing up for a free developer account at developer.webex.com

## Additional Details

- [Blog Post](https://0x2142.com/webex-chatbot-with-adaptivecards/)
- [YouTube Video](https://youtu.be/q4LaBvMePTw)
