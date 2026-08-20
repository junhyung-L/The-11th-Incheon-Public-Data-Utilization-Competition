# Fallin: A GIS Prototype for Older-Pedestrian Fall-Risk Mapping

[English](PORTFOLIO.md) | [한국어](PORTFOLIO.ko.md)

## At a glance

Fallin starts with a practical question: can terrain, pedestrian-environment, and weather conditions identify outdoor segments that deserve an earlier safety warning for older pedestrians? The competition proposal describes a broader service—risk maps, safer routing, caregiver alerts, and smartphone fall detection. The implemented repository covers a narrower, concrete prototype: score GIS segments with explicit rules and render an interactive Folium map.

The proposal’s role table lists Junhyung Lee as CTO / overall software-development lead. The code implements Shapefile loading and CRS conversion, KMA weather retrieval or a demo fallback, rule-based scoring, and HTML map generation. Push alerts, sensor detection, and safer-route routing are proposed product features, not completed or validated repository features.

## Scope: environmental risk, not a clinical prediction

Falls also depend on medical history, medication, strength, balance, and individual behaviour. This prototype deliberately restricts itself to publicly observable outdoor conditions rather than claiming an individual clinical risk score. Its output is a relative risk score for a pedestrian segment.

| Signal group | Examples used in code | Intended role |
|---|---|---|
| Terrain | mean slope degree | capture walking burden on gradients |
| Pedestrian environment | risk-element count and illuminance | represent pavement and visibility conditions |
| Weather | temperature, humidity, precipitation, snow, wind | represent weather-related slip or freeze conditions |
| Spatial representation | segment geometry and centroids | make priorities inspectable on a map |

## Implemented pipeline

`main.py` follows a direct workflow:

```text
Shapefile → GeoPandas load / EPSG:4326 conversion → weather fields → rule score per segment → Folium HTML map
```

`GISDataLoader` refuses a source without a coordinate reference system and converts valid inputs to WGS84 for display. `WeatherFetcher` retrieves `TMP`, `REH`, `PTY`, `PCP`, `SNO`, and `WSD` from the KMA forecast API when `KMA_SERVICE_KEY` is set. Without a key—or after a failed request—it returns a fixed winter-precipitation scenario so the demo can still run.

`RiskCalculator` makes the scoring assumptions visible. A slope above 7 degrees adds five points; a slope above 5 adds three. Three or more recorded risk elements add five points, while one or more add three. Cold temperature, high humidity, precipitation, snowfall, and high wind also contribute. Scores are grouped as Low (0–5), Medium (6–10), and High (11–20). `MapVisualizer` draws all segments as a heatmap and marks high-risk centroids in red.

The deterministic weather fallback makes demonstration possible, but it does not represent the weather at a real historical moment. API use and timestamp need to be recorded when interpreting a generated map.

## From proposal to prototype

The proposal considers KMA forecasts, Incheon mobility datasets, road illuminance/temperature/humidity/foot-traffic data, a fall-incident API, and KOSIS statistics. The implementation reads `mean_slope_degree`, `risk_count`, an illuminance field when present, and weather fields. The proposal also includes an Inju-daero map example and an on-site observation that a yellow-labelled area contained a crosswalk curb and overpass stairs.

The wider service plan includes a 500 m risk map, senior-friendly UI, caregiver notifications, alternative routes, prevention content, and B2C/B2G delivery. That is valuable product and policy framing, but proposed subscription, user-growth, accuracy, and fall-reduction numbers in the report are plans or targets, not measured outcomes from this codebase.

## Honest result boundary and next step

The output is an HTML map that assigns a score and risk level to supplied GIS segments. The repository does not retain complete Shapefile sidecars and provenance, incident labels, route outcomes, or field-validation logs. The weights are design assumptions, not coefficients calibrated against observed falls. It therefore cannot support claims that it predicts falls at a stated accuracy or that its routes reduce accidents.

What is implemented is still a meaningful prototype: it links spatial data, changing weather inputs, transparent rules, and a readable map. The next iteration should retain complete data provenance, join governed incident or safety records spatially, validate with time/spatial separation, record API calls, and test the proposed app features independently.

## Evidence

- [Competition proposal](reports/fallin_incheon_open_data.pdf)
- [Pipeline entry point](main.py)
- [Risk rules](src/risk_calculator.py)
- [GIS loader](src/data_loader.py), [weather module](src/weather.py), and [map visualiser](src/map_visualizer.py)
