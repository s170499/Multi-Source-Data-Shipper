import yaml
import requests
import csv
import json
import time
import logging
from typing import List, Dict, Any
from abc import ABC, abstractmethod

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Abstract base class for data sources
class DataSource(ABC):
    @abstractmethod
    def fetch_data(self, cities: List[str]) -> List[Dict[str, Any]]:
        pass

# OpenWeatherMap source
class OpenWeatherMapSource(DataSource):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def fetch_data(self, cities: List[str]) -> List[Dict[str, Any]]:
        results = []
        for city in cities:
            try:
                params = {"q": city, "appid": self.api_key, "units": "metric"}
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                results.append({
                    "city": city,
                    "temperature_celsius": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "source_provider": "openweathermap"
                })
            except requests.RequestException as e:
                logger.error(f"Error fetching data for {city} from OpenWeatherMap: {e}")
        return results

# WeatherAPI.com source
class WeatherAPISource(DataSource):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1/current.json"

    def fetch_data(self, cities: List[str]) -> List[Dict[str, Any]]:
        results = []
        for city in cities:
            try:
                params = {"key": self.api_key, "q": city}
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                results.append({
                    "city": city,
                    "temperature_celsius": data["current"]["temp_c"],
                    "description": data["current"]["condition"]["text"],
                    "source_provider": "weatherapi"
                })
            except requests.RequestException as e:
                logger.error(f"Error fetching data for {city} from WeatherAPI: {e}")
        return results

# CSV file source
class CSVSource(DataSource):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def fetch_data(self, cities: List[str]) -> List[Dict[str, Any]]:
        results = []
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["city"] in cities:
                        results.append({
                            "city": row["city"],
                            "temperature_celsius": float(row["temperature"]),
                            "description": row["description"],
                            "source_provider": "weather_data.csv"
                        })
        except Exception as e:
            logger.error(f"Error reading CSV file {self.file_path}: {e}")
        return results

# Data Shipper
class DataShipper:
    def __init__(self, listener_host: str, shipping_token: str):
        self.endpoint = f"https://{listener_host}:8071/?token={shipping_token}"
        self.headers = {"Content-Type": "application/json"}

    def ship_data(self, data: List[Dict[str, Any]]) -> None:
        if not data:
            logger.info("No data to ship")
            return
        try:
            # Create newline-delimited JSON
            payload = "\n".join(json.dumps(record) for record in data)
            response = requests.post(self.endpoint, headers=self.headers, data=payload)
            response.raise_for_status()
            logger.info(f"Successfully shipped {len(data)} records to Logz.io")
        except requests.RequestException as e:
            logger.error(f"Error shipping data to Logz.io: {e}")

# Main application
class WeatherDataApp:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        self.polling_interval = self.config["polling_interval"]
        self.shipper = DataShipper(
            self.config["logzio"]["listener_host"],
            self.config["logzio"]["shipping_token"]
        )
        self.sources = self._initialize_sources()

    def _initialize_sources(self) -> List[DataSource]:
        sources = []
        for source_config in self.config["sources"]:
            source_type = source_config["type"]
            if source_type == "openweathermap":
                sources.append(OpenWeatherMapSource(source_config["api_key"]))
            elif source_type == "weatherapi":
                sources.append(WeatherAPISource(source_config["api_key"]))
            elif source_type == "csv":
                sources.append(CSVSource(source_config["file_path"]))
            else:
                logger.warning(f"Unknown source type: {source_type}")
        return sources

    def run(self):
        while True:
            all_data = []
            for source_config, source in zip(self.config["sources"], self.sources):
                data = source.fetch_data(source_config["cities"])
                all_data.extend(data)
        # Print all unified JSON objects
            logger.info(f"Collected {len(all_data)} records:")
            for record in all_data:
                logger.info(f"Unified JSON: {json.dumps(record, indent=2)}")
            self.shipper.ship_data(all_data)
            logger.info(f"Waiting {self.polling_interval} seconds until next poll")
            time.sleep(self.polling_interval)
    

if __name__ == "__main__":
    app = WeatherDataApp("config.yaml")
    app.run()
