# Water Quality Classification & Prediction System

## Project Overview
A comprehensive machine learning system to classify water quality and predict Water Quality Index (WQI) using data from Telangana Control Board.

## Features
- **Water Quality Classification**: Classify water into Safe/Potable, Polluted, and Highly Polluted categories
- **WQI Prediction**: Calculate and predict Water Quality Index
- **Multiple ML Models**: Random Forest, XGBoost, and Neural Networks
- **Feature Importance Analysis**: Identify key parameters affecting water quality
- **Comprehensive Visualizations**: Interactive plots and insights

## Tech Stack
- Python 3.8+
- Scikit-learn
- XGBoost
- TensorFlow/Keras
- Pandas, NumPy
- Matplotlib, Seaborn, Plotly

## Dataset
- **Source**: Telangana Control Board
- **Monitoring Stations**: 215+
- **Parameters**: 37+ water quality parameters including pH, DO, BOD, COD, Coliform counts, etc.
- **Water Bodies**: Rivers (Godavari, Krishna, Musi, Manjeera) and Lakes/Tanks

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
jupyter lab water_quality_analysis.ipynb
```

## Project Structure
```
water-quality/
├── Water_Quality_Data_06_2025.csv
├── water_quality_analysis.ipynb
├── requirements.txt
├── README.md
└── models/ (generated after training)
```

## Key Parameters Analyzed
- Dissolved Oxygen (DO)
- pH
- Biochemical Oxygen Demand (BOD)
- Chemical Oxygen Demand (COD)
- Fecal Coliform
- Total Coliform
- Nitrates & Nitrites
- Total Dissolved Solids (TDS)
- Turbidity

## Results
Results and model performance metrics will be available after running the analysis notebook.

## Author
Water Quality Analysis Project - Telangana Region

