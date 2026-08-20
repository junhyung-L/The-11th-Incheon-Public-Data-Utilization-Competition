"""Command-line entry point for the Fallin heuristic-risk map prototype."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from src.config import DATA_DIR, DEFAULT_SHAPEFILE, result_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a Fallin heuristic-risk map from a pedestrian shapefile.")
    parser.add_argument("--shapefile", default=DEFAULT_SHAPEFILE)
    parser.add_argument("--output-html", type=Path, default=result_path("fall_risk_visualization.html"))
    parser.add_argument("--log-file", type=Path, default=result_path("risk_analysis.log"))
    return parser


def configure_logging(log_file: Path) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_file, encoding="utf-8")],
        force=True,
    )


def main(args: argparse.Namespace) -> None:
    from src.data_loader import GISDataLoader
    from src.map_visualizer import MapVisualizer
    from src.risk_calculator import RiskCalculator
    from src.weather import WeatherFetcher

    configure_logging(args.log_file)
    logging.info("Starting Fall Risk Analysis Pipeline")
    gdf = GISDataLoader(DATA_DIR).load_shapefile(args.shapefile)
    weather_data = WeatherFetcher().fetch_current_weather()
    scored = RiskCalculator(weather_data).apply_risk_modeling(gdf)
    MapVisualizer(scored).generate_map(args.output_html)
    logging.info("Pipeline completed: %s", args.output_html)
    print(scored[["risk_score", "risk_level"]].value_counts().sort_index())


if __name__ == "__main__":
    main(build_parser().parse_args())
