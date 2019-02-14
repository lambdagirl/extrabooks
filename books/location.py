from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="extrabooks_app")

def get_city_location(city):
    location = geolocator.geocode(city)
    longitude = location.longitude
    latitude = location.latitude
    city_location = Point(longitude,latitude,srid=4326)
    return city_location
