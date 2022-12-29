# masto-random-weather
Python3 script that generates a random location, collects the location's weather data and human-readable name, and makes a Mastodon post concluding in whether green beans could grow at the given temperature.

Requires a corresponding `secrets.py` file with the following information:
  ```py
  weather_api_key = "api_key"
  geocode_api_key = "api_key"
  mastodon_api_base_url = "https://some.mastodon.instance/"
  mastodon_client_access_token = "token"
  ```

_Implementation: https://social.validpostage.com/@GreenBeanWeather_
