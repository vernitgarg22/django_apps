from django.test import Client
from django.test import TestCase

import tests.disabled

import weather_info.views


class WeatherInfoTests(TestCase):

    def test_get_weather_info(self):
        c = Client()

        response = c.get('/weather_info/latest/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)

    def test_get_weather_info_with_params(self):
        c = Client()

        lat="42.331427"
        lon="-83.045754"

        response = c.get('/weather_info/latest/?lat={}&lon={}'.format(lat, lon))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)