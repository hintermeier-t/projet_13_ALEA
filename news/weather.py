# - Built-in modules
import os

# - Venv modules
import geoip2.database
from geoip2.errors import AddressNotFoundError
import requests

class WeatherWidget():
    def __init__ (self, ip):
        try:
            with geoip2.database.Reader('geoip/GeoLite2-City.mmdb') as reader:
                geolocation = reader.city(ip)
                self.lat = str(geolocation.location.latitude)
                self.lon = str(geolocation.location.longitude)
        except AddressNotFoundError:
            self.lat = '48.866667'
            self.lon = '2.333333'
        except ValueError:
            self.lat = '48.866667'
            self.lon = '2.333333'
    def update(self):
        self.url= "https://api.openweathermap.org/data/2.5/onecall?"
        self.params = {
            'lat' : self.lat,
            'lon' : self.lon,
            'appid' : os.getenv('WEATHER_KEY'),
            'units' : 'metric'
        }
        query = requests.get(self.url, self.params).json()
        self.weather = query['current']
        self.icon = (
            'http://openweathermap.org/img/wn/'
            + self.weather['weather'][0]['icon']
            + '@2x.png'
            )
        self.temp = self.weather['temp']
        self.pressure =  self.weather['pressure']
        self.humidity =  self.weather['humidity']
        self.wind_speed =  self.weather['wind_speed']
        self.desription = self.weather['weather'][0]['description']

        
        