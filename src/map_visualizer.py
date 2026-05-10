import logging
import folium
from folium.plugins import HeatMap

class MapVisualizer:
    """Handles generation of interactive Folium maps for risk visualization."""
    def __init__(self, gdf):
        self.gdf = gdf

    def generate_map(self, output_html: str = "risk_map.html"):
        """Generates an interactive Folium map with risk visualization."""
        if self.gdf is None:
            logging.error("No data available to map.")
            return

        logging.info("Generating interactive map...")
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
