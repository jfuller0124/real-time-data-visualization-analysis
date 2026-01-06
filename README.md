# Data Visualization Performance Analysis
This repository contains the data visualization and performance analysis work from my senior capstone project, focused on evaluating real-time sensor data display for an embedded composite structure.

## Purpose
Verify that the visualization pipeline can display live sensor data with minimal
latency and sufficient frame rate for real-time interpretation.

## Tools Used
- Python 3.12
- Matplotlib (2D visualization)
- PyVista (3D deformation visualization)
- NumPy

## Method
Simulated strain and temperature data were streamed at 20 Hz to replicate planned
ESP32 sensor output rates. Frame render time, FPS, and data-to-display lag were
measured using Python's perf_counter().

## Key Results
| Library | Avg Render (ms) | FPS | Lag (ms) |
|--------|-----------------|-----|---------|
| Matplotlib | 71.24 | 14.04 | 72.59 |
| PyVista | 1.55 | 643.6 | 2.21 |

## Conclusion
Both visualization methods exceeded real-time requirements (>10 FPS, <200 ms lag).
PyVista demonstrated near-instantaneous rendering suitable for live 3D deformation
mapping, while Matplotlib provided reliable 2D trend visualization.

## How to Run
```bash
pip install pyvista matplotlib numpy
python viz_benchmark.py
