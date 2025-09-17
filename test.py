import unittest
from unittest.mock import patch, mock_open
from DataShipper import OpenWeatherMapSource, WeatherAPISource, CSVSource, WeatherDataApp

class TestWeatherDataTransformation(unittest.TestCase):

    @patch("DataShipper.requests.get")
    def test_openweathermap_fetch_data(self, mock_get):
        # Mock API response
        mock_get.return_value.json.return_value = {
            "main": {"temp": 25},
            "weather": [{"description": "clear sky"}]
        }
        mock_get.return_value.raise_for_status = lambda: None

        source = OpenWeatherMapSource(api_key="fake_api_key")
        data = source.fetch_data(["London"])
        
        expected = [{
            "city": "London",
            "temperature_celsius": 25,
            "description": "clear sky",
            "source_provider": "openweathermap"
        }]
        self.assertEqual(data, expected)

    @patch("DataShipper.requests.get")
    def test_weatherapi_fetch_data(self, mock_get):
        # Mock API response
        mock_get.return_value.json.return_value = {
            "current": {"temp_c": 18, "condition": {"text": "rain"}}
        }
        mock_get.return_value.raise_for_status = lambda: None

        source = WeatherAPISource(api_key="fake_api_key")
        data = source.fetch_data(["Paris"])

        expected = [{
            "city": "Paris",
            "temperature_celsius": 18,
            "description": "rain",
            "source_provider": "weatherapi"
        }]
        self.assertEqual(data, expected)

    @patch("builtins.open", new_callable=mock_open, read_data="city,temperature,description\nTokyo,30,sunny\n")
    def test_csv_fetch_data(self, mock_file):
        source = CSVSource(file_path="fake.csv")
        data = source.fetch_data(["Tokyo"])
        expected = [{
            "city": "Tokyo",
            "temperature_celsius": 30.0,
            "description": "sunny",
            "source_provider": "weather_data.csv"
        }]
        self.assertEqual(data, expected)

if __name__ == "__main__":
    unittest.main()
