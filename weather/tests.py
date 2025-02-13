from django.test import TestCase
from .views import get_weather

class WeatherTests(TestCase):
    def test_weather_api(self):
        city = "London"
        data = get_weather(city)
        self.assertIsNotNone(data)
        self.assertIn("temperature", data)
