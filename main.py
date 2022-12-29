import random
import requests
from mastodon import Mastodon

import secrets


class Location:
    def __init__(self):
        self.latitude = None
        self.longitude = None
        self.weather_short_description = None
        self.temperature_but_feels_like = None
        self.green_bean_status = None
        self.full_name = ''

        while self.full_name == '':
            try:
                self.get_coords()
                self.get_weather_and_name()
                self.reverse_geocode()
            except AttributeError:  # raised when weather or reverse-geocode fail
                continue

    def __str__(self):
        string = (f"Right now in {self.full_name}, it is currently {self.temperature_but_feels_like} "
                  f"They are experiencing {self.weather_short_description.lower()}."
                  f"\n\n{self.green_bean_status}"
                  )
        return string

    def get_coords(self):
        self.latitude = str(round(random.uniform(-45, 83), 3))
        self.longitude = str(round(random.uniform(-180, 180), 3))

    def get_weather_and_name(self):
        """takes a location, either str ("city") or  list ("lat", "lon") and sets appropriate class variables"""
        lat, lon = self.latitude, self.longitude
        units = "metric"
        api_key = secrets.weather_api_key
        query_url = f"http://api.openweathermap.org/data/2.5/weather?appid={api_key}&lat={lat}&lon={lon}&units={units}"

        weather_response = requests.get(query_url).json()

        if weather_response["cod"] != "404":
            self.weather_short_description = weather_response["weather"][0]["description"]

            temp = round(weather_response["main"]["temp"])
            feels_temp = round(weather_response["main"]["feels_like"])

            if temp == feels_temp:
                temp_string = f"{temp} °C, and it sure feels like it!"
            else:
                temp_string = f"{temp} °C, but it feels like {feels_temp} °C."
            self.temperature_but_feels_like = temp_string

            if temp < 13:
                self.green_bean_status = "Green beans cannot grow in this temperature."
            elif 13 <= temp < 18:
                self.green_bean_status = "Green beans might grow in this temperature."
            elif 18 <= temp < 30:
                self.green_bean_status = "Green beans can grow in this temperature!"
            else:
                self.green_bean_status = "Green beans cannot grow in this temperature."

        else:
            raise AttributeError

    def reverse_geocode(self):
        lat, lon = self.latitude, self.longitude
        api_key = secrets.geocode_api_key
        query_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&result_type=political&key={api_key}"

        geocode_response = requests.get(query_url).json()

        if geocode_response["status"] == "OK":
            address_components = geocode_response["results"][0]["address_components"]
            long_names = [d["long_name"] for d in address_components if "political" in d["types"]]
            pretty_name = ", ".join(long_names[1:])
            self.full_name = pretty_name

        else:
            raise AttributeError


def main():
    # log into social.validpostage.com
    mastodon = Mastodon(
        access_token=secrets.mastodon_client_access_token,
        api_base_url=secrets.mastodon_api_base_url
    )

    location = Location()

    mastodon.status_post(str(location))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
