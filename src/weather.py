import logging
import requests
import xmltodict
from datetime import datetime

class WeatherFetcher:
    """Handles fetching real-time weather data from KMA API or fallback sources."""
    def __init__(self, api_key: str = None):
        self.api_key = api_key or "rP3MkYGETA69zJGBhPwOnA"

    def fetch_current_weather(self, nx: int = 55, ny: int = 124) -> dict:
        """Fetches short-term weather forecast from KMA API."""
        logging.info("Fetching real-time weather data from KMA API...")
        url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
        
        base_date = datetime.now().strftime("%Y%m%d")
        base_time = "0600" # Fallback fixed time
        
        params = {
            'serviceKey': self.api_key,
            'pageNo': '1',
            'numOfRows': '1000',
            'dataType': 'XML',
            'base_date': base_date,
            'base_time': base_time,
            'nx': str(nx),
            'ny': str(ny)
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = xmltodict.parse(response.text)
                items = data['response']['body']['items']['item']
                
                weather = {}
                for item in items:
                    category = item['category']
                    value = item['fcstValue']
                    weather[category] = value
                
                logging.info(f"Weather data fetched successfully.")
                return weather
            else:
                logging.warning(f"API request failed with status: {response.status_code}. Using fallback.")
                return self._get_fallback_weather()
        except Exception as e:
            logging.error(f"Error fetching weather data: {e}. Using fallback.")
            return self._get_fallback_weather()

    def _get_fallback_weather(self) -> dict:
        """Provides default weather conditions for simulation."""
        logging.info("Using fallback standard winter weather conditions.")
        return {
            'TMP': '0',   # 0 degrees Celsius
            'REH': '95',  # High humidity
            'PTY': '1',   # Rain/Snow
            'PCP': '1.0', # 1mm precipitation
            'SNO': '1.0', # 1cm snow
            'WSD': '6.0'  # High wind speed
        }
