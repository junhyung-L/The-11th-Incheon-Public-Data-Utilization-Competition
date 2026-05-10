import os
import logging
import geopandas as gpd

class GISDataLoader:
    """Handles loading and preprocessing of GIS Shapefiles."""
    def __init__(self, data_path: str):
        self.data_path = data_path

    def load_shapefile(self, filename: str, target_crs: str = 'EPSG:4326') -> gpd.GeoDataFrame:
        """Loads a shapefile and ensures it matches the target CRS."""
        full_path = os.path.join(self.data_path, filename)
        logging.info(f"Loading GIS data from {full_path}...")
        
        try:
            gdf = gpd.read_file(full_path, encoding='utf-8')
            logging.info(f"Loaded {len(gdf)} records.")
            
            if gdf.crs != target_crs:
                logging.info(f"Converting CRS from {gdf.crs} to {target_crs}")
                gdf = gdf.to_crs(target_crs)
                
            return gdf
        except Exception as e:
            logging.error(f"Failed to load GIS data: {e}")
            raise
