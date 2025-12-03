# 🌊 Water Quality Classification & Prediction System

> AI-powered water quality analysis and prediction system for Telangana using Machine Learning

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13+-orange.svg)](https://tensorflow.org/)
[![GitHub Pages](https://img.shields.io/badge/demo-online-brightgreen.svg)](https://yourusername.github.io/water-quality/)

## Overview

A comprehensive machine learning system that analyzes water quality data from 213 monitoring stations across Telangana, classifies water into three categories (Safe/Potable, Polluted, Highly Polluted), and predicts Water Quality Index (WQI) using multiple AI models.

### [**Live Dashboard**](https://arvind-55555.github.io/Telangana-Water-Quality-Prediction/) | [**Documentation**](documentation/) | [**Notebook**](src/notebooks/)

## Features

- 🤖 **6 ML Models**: Random Forest, XGBoost, Neural Networks (Classification & Regression)
- 📊 **Interactive Dashboard**: Real-time visualizations and statistics
- 🎯 **93.94% Accuracy**: Best-in-class water quality classification
- 📈 **WQI Prediction**: R² = 0.919 for continuous quality assessment
- 🌍 **Real Data**: 213 monitoring stations, 165 validated samples
- 🚀 **Production Ready**: Complete API and deployment scripts

## Project Structure

```
water-quality/
├── 📂 docs/                          # GitHub Pages website
│   ├── index.html                    # Interactive dashboard
│   ├── css/style.css                 # Styling
│   └── js/main.js                    # Visualizations
│
├── 📂 src/                           # Source code
│   ├── predict_water_quality.py      # Prediction API
│   ├── notebooks/                    # Analysis notebooks
│   │   └── water_quality_analysis.ipynb
│   └── utils/                        # Utility functions
│
├── 📂 models/                        # Trained ML models (3.3 MB)
│   ├── rf_classifier.pkl             # Random Forest classifier
│   ├── xgb_classifier.pkl            # XGBoost classifier
│   ├── nn_classifier.keras           # Neural Network classifier
│   ├── rf_regressor.pkl              # Random Forest regressor
│   ├── xgb_regressor.pkl             # XGBoost regressor
│   └── nn_regressor.keras            # Neural Network regressor
│
├── 📂 scripts/                       # Automation scripts
│   ├── run_analysis.py               # Complete analysis pipeline
│   └── quickstart.sh                 # Quick setup script
│
├── 📂 documentation/                 # Project documentation
│   ├── README.md                     # Main documentation
│   ├── USAGE_GUIDE.md                # Usage instructions
│   ├── PROJECT_SUMMARY.md            # Detailed summary
│   ├── BUGFIX.md                     # Bug fixes log
│   └── EXECUTION_SUMMARY.md          # Execution report
│
├── Water_Quality_Data_06_2025.csv    # Dataset (Telangana PCB)
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## Quick Start

### Option 1: Web Dashboard (No Installation)
Visit the [**Live Dashboard**](https://yourusername.github.io/water-quality/) to explore visualizations and results.

### Option 2: Run Locally

```bash
# Clone repository
git clone https://github.com/yourusername/water-quality.git
cd water-quality

# Install dependencies
pip install -r requirements.txt

# Run complete analysis
python scripts/run_analysis.py

# Make predictions
python src/predict_water_quality.py
```

### Option 3: Use Pre-trained Models

```python
from src.predict_water_quality import WaterQualityPredictor

# Initialize predictor
predictor = WaterQualityPredictor()

# Your water sample
sample_data = {
    'DO (mg/L)': 6.5,
    'pH': 7.8,
    'BOD (mg/L)': 2.5,
    'COD (mg/L)': 25,
    'Total Coliform (MPN/100ml)': 30,
    'TDS (mg/L)': 400,
    # ... other parameters
}

# Get predictions
results = predictor.predict_all(sample_data)
print(results)
```

## Results & Performance

### Classification Models (Accuracy)
| Model | Accuracy | Best For |
|-------|----------|----------|
| **XGBoost** | 93.94% | ⭐ Production use |
| **Random Forest** | 90.91% | Feature importance |
| **Neural Network** | 87.88% | Complex patterns |

### Regression Models (WQI Prediction)
| Model | R² Score | RMSE | Best For |
|-------|----------|------|----------|
| **XGBoost** | 0.919 | 3.30 | ⭐ Accurate predictions |
| **Random Forest** | 0.915 | 3.37 | Interpretability |
| **Neural Network** | - | - | (Needs more data) |

### Water Quality Status (Telangana, June 2025)
- 🟢 **Safe/Potable**: 1.8% (3 samples)
- 🟡 **Polluted**: 71.5% (118 samples)
- 🔴 **Highly Polluted**: 26.7% (44 samples)
- **Average WQI**: 46.20 (Moderate Pollution)

## Methodology

### Data Source
- **Provider**: Telangana Pollution Control Board
- **Period**: June 2025
- **Stations**: 213 monitoring locations
- **Water Bodies**: Rivers (Godavari, Krishna, Musi, Manjeera) + Lakes/Tanks

### Parameters Analyzed (18)
- Physical: pH, DO, Conductivity, Turbidity, TDS, TSS
- Chemical: BOD, COD, Nitrate, Nitrite, Ammonia, Chloride, Hardness, Fluoride
- Biological: Total Coliform, Fecal Coliform
- Others: Total Alkalinity, Total Phosphate

### WQI Calculation
Based on WHO/BIS drinking water standards with weighted averaging:
- **Safe/Potable**: WQI ≥ 70
- **Polluted**: 40 ≤ WQI < 70
- **Highly Polluted**: WQI < 40

## Technology Stack

### Backend
- **Python 3.8+**
- **TensorFlow 2.13+** - Neural Networks
- **XGBoost 1.7+** - Gradient Boosting
- **Scikit-learn 1.3+** - Random Forest & preprocessing
- **Pandas, NumPy** - Data manipulation

### Frontend (Dashboard)
- **HTML5, CSS3, JavaScript**
- **Chart.js 4.4** - Interactive visualizations
- **Font Awesome 6.4** - Icons
- **Responsive Design** - Mobile-friendly

### Deployment
- **GitHub Pages** - Web dashboard
- **Jupyter Notebooks** - Analysis environment
- **Python Scripts** - Automation

## Key Insights

### Most Critical Parameters
1. **Total Coliform** (18% importance) - Bacterial contamination indicator
2. **Fecal Coliform** (16% importance) - Sewage pollution indicator
3. **BOD** (14% importance) - Organic pollution load
4. **COD** (12% importance) - Chemical oxygen demand
5. **Dissolved Oxygen** (11% importance) - Aquatic life indicator

### Most Polluted Water Bodies
- River Musi (urban stretch)
- Lakes near industrial areas
- Urban tanks with sewage inflow

### Recommendations
- 🎯 **Priority**: Focus on 44 highly polluted locations
- 🔬 **Monitoring**: Increase frequency for coliform and BOD
- 🏭 **Industrial**: Strengthen effluent treatment requirements
- 👥 **Community**: Public awareness and participation programs

## Deployment

### GitHub Pages (Automated)
The `docs/` folder automatically deploys to:
```
https://yourusername.github.io/water-quality/
```

### Manual Deployment
```bash
# Build and deploy
git add docs/
git commit -m "Update dashboard"
git push origin main

# GitHub Actions will auto-deploy to Pages
```

## Documentation

- [**Usage Guide**](documentation/USAGE_GUIDE.md) - Detailed usage instructions
- [**Project Summary**](documentation/PROJECT_SUMMARY.md) - Complete overview
- [**Execution Summary**](documentation/EXECUTION_SUMMARY.md) - Implementation details
- [**Bug Fixes**](documentation/BUGFIX.md) - Issues resolved

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Telangana Pollution Control Board** - Data source
- **WHO/BIS** - Water quality standards
- **Open Source Community** - Amazing ML libraries

## Contact

- **Issues**: [GitHub Issues](https://github.com/Arvind-55555/Telangana-Water-Quality-Prediction/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Arvind-55555/Telangana-Water-Quality-Prediction/discussions)

## 🎓 Citation

If you use this project in your research, please cite:

```bibtex
@software{water_quality_2025,
  title = {Water Quality Classification & Prediction System},
  author = {Arvind},
  year = {2025},
  url = {https://github.com/Arvind-55555/Telangana-Water-Quality-Prediction}
}
```

---

<div align="center">

**Star this repo if you find it useful!**


[Report Bug](https://github.com/Arvind-55555/Telangana-Water-Quality-Prediction/issues) · [Request Feature](https://github.com/Arvind-55555/Telangana-Water-Quality-Prediction/issues) · [Documentation](documentation/)

</div>

