"""Portable paths and runtime settings for the Fallin prototype."""

from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.getenv("FALLIN_DATA_DIR", PROJECT_ROOT / "data"))
RESULTS_DIR = Path(os.getenv("FALLIN_RESULTS_DIR", PROJECT_ROOT / "results"))
WEATHER_API_KEY = os.getenv("KMA_SERVICE_KEY")
DEFAULT_SHAPEFILE = os.getenv("FALLIN_SHAPEFILE", "인도_조도_경사도.shp")


def result_path(filename: str) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    return RESULTS_DIR / filename
