import logging
import pandas as pd

class RiskCalculator:
    """Implements the heuristic risk scoring logic for elderly falls."""
    def __init__(self, weather_data: dict):
        self.weather_data = weather_data

    def calculate_score(self, row) -> int:
        """Calculates risk score for a single row/segment."""
        score = 0
        w = self.weather_data

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

        # 2. Terrain & Environment Factors
        try:
            slope = float(row.get('mean_slope_degree', 0))
            if slope > 7: score += 5
            elif slope > 5: score += 3
            
            lux = row.get('조도', '밝음')
            if lux in ['낮음', '어두움']: score += 1
            
            risk_count = float(row.get('risk_count', 0))
            if risk_count >= 3: score += 5
            elif risk_count >= 1: score += 3
        except Exception as e:
            logging.debug(f"GIS scoring error: {e}")

        return score

    def apply_risk_modeling(self, gdf) -> pd.DataFrame:
        """Applies risk scoring to the entire GeoDataFrame and categorizes levels."""
        logging.info("Calculating risk scores for all segments...")
        gdf['risk_score'] = gdf.apply(self.calculate_score, axis=1)
        
        gdf['risk_level'] = pd.cut(
            gdf['risk_score'],
            bins=[-1, 5, 10, 20],
            labels=['Low', 'Medium', 'High']
        )
        return gdf
