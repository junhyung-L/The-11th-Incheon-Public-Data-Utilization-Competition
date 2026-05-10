"""
Fall Risk Analysis - Main Orchestrator
=====================================

This script orchestrates the full pipeline for elderly fall risk analysis,
importing modules from the src/ directory.
"""

import os
import logging
from src.data_loader import GISDataLoader
from src.weather import WeatherFetcher
from src.risk_calculator import RiskCalculator
from src.map_visualizer import MapVisualizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('risk_analysis.log', encoding='utf-8')
    ]
)

def main():
    DATA_DIR = "./data"
    SHP_FILE = "인도_조도_경사도.shp"
    OUTPUT_MAP = "fall_risk_visualization.html"

    logging.info("Starting Fall Risk Analysis Pipeline...")

    # 1. Load Data
    loader = GISDataLoader(DATA_DIR)
    gdf = loader.load_shapefile(SHP_FILE)

    # 2. Fetch Weather
    weather_fetcher = WeatherFetcher()
    weather_data = weather_fetcher.fetch_current_weather()

    # 3. Calculate Risk
    calculator = RiskCalculator(weather_data)
    gdf = calculator.apply_risk_modeling(gdf)

    # 4. Visualize
    visualizer = MapVisualizer(gdf)
    visualizer.generate_map(OUTPUT_MAP)

    logging.info("Pipeline completed successfully!")
    print(gdf[['risk_score', 'risk_level']].value_counts().sort_index())

if __name__ == "__main__":
    main()
