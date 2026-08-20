import logging
from pathlib import Path
import geopandas as gpd

class GISDataLoader:
    """Handles loading and preprocessing of GIS Shapefiles."""
    def __init__(self, data_path: str | Path):
        self.data_path = Path(data_path)

    def load_shapefile(self, filename: str, target_crs: str = 'EPSG:4326') -> gpd.GeoDataFrame:
        """Loads a shapefile and ensures it matches the target CRS."""
        full_path = self.data_path / filename
        if not full_path.is_file():
            raise FileNotFoundError(f"Shapefile not found: {full_path}")
        logging.info(f"Loading GIS data from {full_path}...")
        
        try:
            gdf = gpd.read_file(full_path, encoding='utf-8')
            logging.info(f"Loaded {len(gdf)} records.")
            
            if gdf.crs is None:
                raise ValueError(f"Input shapefile has no CRS: {full_path}")
            if gdf.crs.to_string() != target_crs:
                logging.info(f"Converting CRS from {gdf.crs} to {target_crs}")
                gdf = gdf.to_crs(target_crs)
                
            return gdf
        except Exception as e:
            logging.error(f"Failed to load GIS data: {e}")
            raise
