"""
Elderly Fall Risk Analysis Pipeline
===================================

This module provides a structured, production-ready pipeline for analyzing and predicting 
elderly fall risks based on GIS data, illuminance, and real-time weather conditions.
Derived from the analysis notebooks of the 11th Incheon Public Data Utilization Competition.

Author: Antigravity (Data Science Consultant Persona)
Date: 2026-05-10
"""

import os
import logging
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
import requests
import xmltodict
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('risk_analysis.log', encoding='utf-8')
    ]
)

class FallRiskPredictor:
    """
    A class to handle the end-to-end pipeline for fall risk prediction.
    """
    def __init__(self, data_path: str, api_key: str = None):
        self.data_path = data_path
        self.api_key = api_key or "rP3MkYGETA69zJGBhPwOnA"  # Default key from notebook
        self.gdf = None
        self.weather_data = {}

    def load_gis_data(self, filename: str):
        """Loads Shapefile containing road, slope, and illuminance data."""
        full_path = os.path.join(self.data_path, filename)
        logging.info(f"Loading GIS data from {full_path}...")
        try:
            self.gdf = gpd.read_file(full_path, encoding='utf-8')
            logging.info(f"Loaded {len(self.gdf)} records.")
            # Ensure CRS is EPSG:4326 for Folium visualization
            if self.gdf.crs != 'EPSG:4326':
                logging.info(f"Converting CRS from {self.gdf.crs} to EPSG:4326")
                self.gdf = self.gdf.to_crs('EPSG:4326')
            return self.gdf
        except Exception as e:
            logging.error(f"Failed to load GIS data: {e}")
            raise

    def fetch_weather_data(self, nx: int = 55, ny: int = 124):
        """
        Fetches short-term weather forecast from KMA API.
        Default coordinates are for Incheon area.
        """
        logging.info("Fetching real-time weather data from KMA API...")
        url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
        
        # In a real production environment, date/time should be dynamic.
        # Using a fixed date/time similar to the notebook for reproducibility or fallback.
        base_date = datetime.now().strftime("%Y%m%d")
        base_time = "0600" # Example fixed time, should be updated dynamically
        
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
                
                # Parse items into a dictionary
                weather = {}
                for item in items:
                    category = item['category']
                    value = item['fcstValue']
                    weather[category] = value
                
                self.weather_data = weather
                logging.info(f"Weather data fetched successfully: {weather}")
                return weather
            else:
                logging.warning(f"API request failed with status: {response.status_code}. Using default fallback.")
                return self._get_fallback_weather()
        except Exception as e:
            logging.error(f"Error fetching weather data: {e}. Using fallback.")
            return self._get_fallback_weather()

    def _get_fallback_weather(self):
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

    def calculate_risk_score(self, row):
        """
        Implements the heuristic risk scoring logic from the notebook.
        """
        score = 0
        w = self.weather_data if self.weather_data else self._get_fallback_weather()

        # 1. Weather Factors
        try:
            if float(w.get('TMP', 20)) <= 0: score += 2
            if float(w.get('REH', 50)) >= 90: score += 1
            if w.get('PTY', '0') in ['1', '2', '3']: score += 2
            if float(w.get('PCP', 0)) > 0: score += 1
            if float(w.get('SNO', 0)) > 0: score += 2
            if float(w.get('WSD', 0)) >= 5: score += 1
        except Exception as e:
            logging.debug(f"Weather scoring error: {e}")

        # 2. Terrain & Environment Factors (from GIS data)
        try:
            slope = float(row.get('mean_slope_degree', 0))
            if slope > 7: score += 5
            elif slope > 5: score += 3
            
            lux = row.get('조도', '밝음')
            # Assuming night time for maximum risk assessment or check time
            if lux in ['낮음', '어두움']: score += 1
            
            # Risk count (if available in joined data)
            risk_count = float(row.get('risk_count', 0))
            if risk_count >= 3: score += 5
            elif risk_count >= 1: score += 3
        except Exception as e:
            logging.debug(f"GIS scoring error: {e}")

        return score

    def process_pipeline(self, shapefile_name: str):
        """Runs the full analysis pipeline."""
        self.load_gis_data(shapefile_name)
        self.fetch_weather_data()
        
        logging.info("Calculating risk scores for all segments...")
        self.gdf['risk_score'] = self.gdf.apply(self.calculate_risk_score, axis=1)
        
        # Categorize risk levels
        self.gdf['risk_level'] = pd.cut(
            self.gdf['risk_score'],
            bins=[-1, 5, 10, 20],
            labels=['Low', 'Medium', 'High']
        )
        
        logging.info("Pipeline processing complete.")
        return self.gdf

    def generate_map(self, output_html: str = "risk_map.html"):
        """Generates an interactive Folium map with risk visualization."""
        if self.gdf is None:
            logging.error("No data available to map. Run pipeline first.")
            return

        logging.info("Generating interactive map...")
        # Center map on the data
        center_lat = self.gdf.geometry.centroid.y.mean()
        center_lon = self.gdf.geometry.centroid.x.mean()
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=14, tiles='cartodbpositron')

        # Add Risk Heatmap
        heat_data = [
            [row.geometry.centroid.y, row.geometry.centroid.x, row['risk_score']]
            for idx, row in self.gdf.iterrows() if not row.geometry.is_empty
        ]
        HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(m)

        # Add high risk areas as circles
        high_risk = self.gdf[self.gdf['risk_level'] == 'High']
        for idx, row in high_risk.iterrows():
            if not row.geometry.is_empty:
                folium.CircleMarker(
                    location=[row.geometry.centroid.y, row.geometry.centroid.x],
                    radius=5,
                    color='red',
                    fill=True,
                    fill_color='red',
                    popup=f"Score: {row['risk_score']}"
                ).add_to(m)

        m.save(output_html)
        logging.info(f"Map saved to {output_html}")
        return m

if __name__ == "__main__":
    # Example usage
    DATA_DIR = "./data"
    SHP_FILE = "인도_조도_경사도.shp"
    
    predictor = FallRiskPredictor(DATA_DIR)
    try:
        results = predictor.process_pipeline(SHP_FILE)
        predictor.generate_map("fall_risk_visualization.html")
        print("\nPipeline executed successfully!")
        print(results[['risk_score', 'risk_level']].value_counts().sort_index())
    except Exception as e:
        print(f"Pipeline failed: {e}")
