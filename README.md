# 📍 11th Incheon Public Data Utilization Competition: Excellence Award 🏆

This repository contains the project for the **'11th Incheon Public Data Utilization Competition'** focused on safety for the elderly.

The project proposes a **"Minimum Risk Route"** service (Fallin) by fusing Incheon city's GIS terrain data, street illuminance (lux), and real-time weather conditions to calculate a **Rule-Based Fall Risk Score** for elderly pedestrians.

---

## 📌 1. Problem Definition (문제 정의)

- **Background**: As society enters a super-aged phase, elderly fall accidents are becoming a critical social issue. Traditional navigation services only offer the shortest path, ignoring safety hazards like steep slopes or slippery roads.
- **Objective**: To develop a data-driven service that calculates and visualizes fall risks on pedestrian paths, providing safer routes for the elderly.
- **Vision**: "Prioritizing Safety Over Speed: A Data-Driven Approach to Preventing Elderly Falls."

## 📊 2. Data Acquisition & Preprocessing (데이터 수집 및 전처리)

- **Multi-Source Data Fusion**:
  - **GIS Data**: Pedestrian paths and contour lines from the Public Data Portal.
  - **Weather Data**: Real-time short-term forecast (Temperature, Precipitation, Humidity) from the Korea Meteorological Administration (KMA) API.
  - **Illuminance Data**: Streetlight and road brightness data (CSV).
- **Refactored Module**: `src/data_loader.py`
  - Handles loading of massive Shapefiles and ensures Coordinate Reference System (CRS) conversion to EPSG:4326 for visualization.

## 🔬 3. Risk Modeling & Methodology (위험도 모델링 및 방법론)

- **Heuristic Baseline Model (규칙 기반 베이스라인 모델)**:
  - **Important Note**: Due to the lack of historical fall incident data (ground truth), this project implements a **heuristic rule-based scoring system** rather than a predictive machine learning model. This serves as a robust baseline for decision support.
  - The Fall Risk Score is calculated dynamically by combining static terrain data with dynamic environmental factors based on domain knowledge.

| Category | Variable | Condition / Weight | Description |
| :--- | :--- | :---: | :--- |
| **Terrain** | Slope Degree | > 7°: +5 points<br>> 5°: +3 points | Calculated from contour lines using DEM interpolation. |
| **Environment** | Illuminance (Lux) | Low / Dark: +1 point | Poor visibility increases risk. |
| **Weather** | Temperature (TMP) | ≤ 0°C: +2 points | Risk of freezing/black ice. |
| | Precipitation (PTY) | Rain/Snow: +2 points | Slippery road surfaces. |
| | Snowfall (SNO) | > 0cm: +2 points | Walking obstruction. |

- **Refactored Module**: `src/risk_calculator.py`
  - Implements the heuristic risk scoring algorithm.

## 🖼️ 4. Visualization & Prototype (시각화 및 프로토타입)

- **Interactive Risk Map**:
  - Developed an interactive risk heatmap using **Folium**.
  - High-risk areas are marked with specific pins to guide policy decisions and pedestrian awareness.
- **Refactored Module**: `src/map_visualizer.py`

### Service Prototype
![Service Prototype](images/서비스프로토타입_이미지.png)
*Figure 1: Concept and UI flow for the Fallin service.*

### Risk Map Visualization
![Map Visualization](images/지도_시각화.png)
*Figure 2: Interactive map showing high-risk areas.*

## 🏁 5. Conclusion & Future Work (결론 및 향후 과제)

- **Outcome**: Successfully mapped the fall risk scores across Incheon's pedestrian network using a rule-based approach.
- **Analytical ROI**:
  - **Social Value**: Provides actionable data for local governments to prioritize safety facility installations and snow removal.
- **Future Work (Next Steps)**:
  - **Transition to Machine Learning**: We plan to acquire actual historical fall incident data from medical centers or emergency services to train a classification model (e.g., XGBoost, Random Forest) to predict the actual probability of falls, moving beyond the heuristic score.
  - **Model Validation**: Use confusion matrix and ROC-AUC to validate the predictive model once ground truth data is available.

---

## 📁 Repository Structure

```text
├── notebooks/                  # Original exploratory Jupyter notebooks
├── src/                        # Refactored production-ready source code
│   ├── data_loader.py          # GIS data loading and CRS conversion
│   ├── weather.py              # KMA API integration
│   ├── risk_calculator.py      # Heuristic risk model
│   └── map_visualizer.py       # Folium heatmap generation
├── images/                     # Project screenshots and diagrams
├── data/                       # GIS Shapefiles (ignored if too large)
└── main.py                     # Master pipeline runner
```

## ⚙️ How to Run

1. Install dependencies:
   ```bash
   pip install pandas geopandas folium requests xmltodict
   ```
2. Run the full pipeline:
   ```bash
   python main.py
   ```

## 👥 Contributors

- **Junhyung L.** (Project Lead / Data Analyst)

---
*Refactored and polished to meet professional software engineering standards for the [Data Analyst Portfolio](https://github.com/junhyung-L).*
