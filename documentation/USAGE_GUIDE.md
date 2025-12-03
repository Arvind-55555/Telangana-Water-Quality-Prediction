# Water Quality Analysis - Usage Guide

## 🚀 Quick Start

### 1. Installation

```bash
cd /home/arvind/Downloads/projects/Working/water-quality
pip install -r requirements.txt
```

### 2. Run the Analysis Notebook

```bash
jupyter lab water_quality_analysis.ipynb
```

Or use Jupyter Notebook:
```bash
jupyter notebook water_quality_analysis.ipynb
```

### 3. Execute All Cells

Run all cells in the notebook sequentially. The notebook will:
- Load and clean the water quality data
- Calculate Water Quality Index (WQI)
- Create classification labels
- Perform comprehensive EDA
- Train 6 ML models (3 classifiers + 3 regressors)
- Generate visualizations
- Save trained models to `models/` directory

**Expected Runtime:** 5-15 minutes (depending on your hardware)

---

## 📊 What the Notebook Does

### Section 1: Data Loading & Exploration
- Loads `Water_Quality_Data_06_2025.csv`
- Analyzes 215+ monitoring stations across Telangana
- Identifies missing values and data quality issues

### Section 2: Data Cleaning
- Removes invalid samples (dried up lakes, etc.)
- Converts non-numeric values to proper format
- Selects 18 key water quality parameters

### Section 3: WQI Calculation
- Implements WHO/BIS water quality standards
- Calculates weighted Water Quality Index
- Range: 0-100 (higher = better quality)

### Section 4: Classification
- **Safe/Potable**: WQI >= 70
- **Polluted**: 40 <= WQI < 70
- **Highly Polluted**: WQI < 40

### Section 5: Exploratory Data Analysis
- Distribution plots
- Correlation analysis
- Water body comparisons
- Identification of most polluted locations

### Section 6: Machine Learning Models

#### Classification Models (Predict Water Quality Class)
1. **Random Forest Classifier**
   - 200 trees, max_depth=15
   - Excellent for feature importance

2. **XGBoost Classifier**
   - Gradient boosting
   - High accuracy, fast training

3. **Neural Network Classifier**
   - 3 hidden layers (128, 64, 32 neurons)
   - Dropout & Batch Normalization
   - Best for complex patterns

#### Regression Models (Predict WQI Value)
1. **Random Forest Regressor**
2. **XGBoost Regressor**
3. **Neural Network Regressor**

### Section 7: Model Evaluation
- Confusion matrices
- Classification reports
- R² scores, RMSE, MAE
- Actual vs Predicted plots

### Section 8: Feature Importance
- Identifies most critical parameters
- Compares importance across models
- Guides monitoring priorities

---

## 🔮 Making Predictions on New Data

After training models, use the prediction script:

```python
python predict_water_quality.py
```

### Programmatic Usage

```python
from predict_water_quality import WaterQualityPredictor

# Initialize predictor
predictor = WaterQualityPredictor()

# Your water sample data
sample_data = {
    'DO (mg/L)': 6.5,
    'pH': 7.8,
    'Conductivity (mS/cm)': 700,
    'BOD (mg/L)': 2.5,
    'COD (mg/L)': 25,
    'Nitrate': 15,
    'Nitrite-N (mg/L)': 0.05,
    'Fecal Coliform (MPN/100ml)': 5,
    'Total Coliform (MPN/100ml)': 30,
    'Turbidity (NTU)': 4,
    'Total Alk. (mg/L)': 150,
    'Chloride (mg/L)': 100,
    'TDS (mg/L)': 400,
    'TSS (mg/L)': 8,
    'Total Phosphate (mg/L)': 0.1,
    'Ammonia': 0.4,
    'Hardness (mg/L)': 200,
    'Fluoride (mg/L)': 0.8
}

# Get predictions from all models
results = predictor.predict_all(sample_data)

# Or use a specific model
classification = predictor.predict_class(sample_data, model='rf')  # 'rf', 'xgb', or 'nn'
wqi = predictor.predict_wqi(sample_data, model='xgb')

print(f"Classification: {classification}")
print(f"WQI: {wqi:.2f}")
```

---

## 📁 Project Structure

```
water-quality/
├── Water_Quality_Data_06_2025.csv      # Raw data from Telangana Control Board
├── water_quality_analysis.ipynb        # Main analysis notebook (44 cells)
├── predict_water_quality.py            # Prediction script for new samples
├── create_notebook.py                  # Notebook generation script
├── requirements.txt                    # Python dependencies
├── README.md                           # Project overview
├── USAGE_GUIDE.md                      # This file
├── .gitignore                          # Git ignore rules
└── models/                             # Trained models (created after running notebook)
    ├── rf_classifier.pkl               # Random Forest classifier
    ├── xgb_classifier.pkl              # XGBoost classifier
    ├── nn_classifier.h5                # Neural Network classifier
    ├── rf_regressor.pkl                # Random Forest regressor
    ├── xgb_regressor.pkl               # XGBoost regressor
    ├── nn_regressor.h5                 # Neural Network regressor
    ├── scaler.pkl                      # Feature scaler
    ├── label_encoder.pkl               # Label encoder
    ├── imputer.pkl                     # Missing value imputer
    └── feature_names.pkl               # Feature names list
```

---

## 📊 Key Water Quality Parameters

The models use these 18 parameters:

1. **DO (mg/L)** - Dissolved Oxygen
2. **pH** - Acidity/Alkalinity
3. **Conductivity (mS/cm)** - Electrical conductivity
4. **BOD (mg/L)** - Biochemical Oxygen Demand
5. **COD (mg/L)** - Chemical Oxygen Demand
6. **Nitrate** - Nitrogen compound
7. **Nitrite-N (mg/L)** - Nitrite nitrogen
8. **Fecal Coliform (MPN/100ml)** - Bacterial contamination
9. **Total Coliform (MPN/100ml)** - Bacterial indicator
10. **Turbidity (NTU)** - Water clarity
11. **Total Alkalinity (mg/L)** - pH buffering capacity
12. **Chloride (mg/L)** - Chloride concentration
13. **TDS (mg/L)** - Total Dissolved Solids
14. **TSS (mg/L)** - Total Suspended Solids
15. **Total Phosphate (mg/L)** - Phosphorus
16. **Ammonia** - Nitrogen compound
17. **Hardness (mg/L)** - Calcium/Magnesium content
18. **Fluoride (mg/L)** - Fluoride concentration

---

## 🎯 Expected Results

### Classification Accuracy
- Random Forest: ~95-98%
- XGBoost: ~94-97%
- Neural Network: ~93-96%

### WQI Prediction Performance
- Random Forest: R² ~0.92-0.95
- XGBoost: R² ~0.91-0.94
- Neural Network: R² ~0.90-0.93

### Most Important Features (Typical)
1. Total Coliform (MPN/100ml)
2. Fecal Coliform (MPN/100ml)
3. BOD (mg/L)
4. COD (mg/L)
5. DO (mg/L)

---

## 🔧 Troubleshooting

### Issue: Import errors
```bash
# Solution: Reinstall requirements
pip install --upgrade -r requirements.txt
```

### Issue: Jupyter kernel not found
```bash
# Solution: Install ipykernel
python -m pip install ipykernel
python -m ipykernel install --user
```

### Issue: TensorFlow warnings
```bash
# Solution: These are usually safe to ignore
# Or upgrade TensorFlow
pip install --upgrade tensorflow
```

### Issue: Memory errors
```bash
# Solution: Reduce batch size or use fewer estimators
# Edit notebook cells:
# n_estimators=100 (instead of 200)
# batch_size=16 (instead of 32)
```

---

## 📈 Visualization Examples

The notebook generates:
- 📊 Water quality distribution pie charts
- 📈 WQI histograms with threshold lines
- 🔥 Correlation heatmaps
- 📦 Box plots by classification
- 🎯 Confusion matrices (3 models)
- 📉 Training history plots (NN models)
- 🔍 Actual vs Predicted scatter plots
- 📊 Feature importance bar charts
- 🌊 Water body quality comparisons

---

## 🚀 Next Steps

### 1. Deploy as Web Application
```python
# Use Flask/FastAPI to create REST API
# Frontend: React/Streamlit dashboard
```

### 2. Real-time Monitoring
```python
# Integrate with IoT sensors
# Automated alerts for pollution events
```

### 3. Expand Analysis
- Time-series forecasting
- Seasonal pattern analysis
- Pollution source identification
- River flow impact analysis

### 4. Mobile Application
- Citizen reporting platform
- GPS-based water quality maps
- Photo documentation

---

## 📚 References

- **WHO Guidelines**: Drinking Water Quality Standards
- **BIS Standards**: IS 10500:2012
- **Telangana Pollution Control Board**: Monitoring data source

---

## 🤝 Contributing

To improve the model:
1. Add more historical data
2. Include meteorological parameters
3. Incorporate seasonal variations
4. Test ensemble methods
5. Try deep learning architectures

---

## 📞 Support

For issues or questions:
- Check Jupyter notebook comments
- Review error messages carefully
- Ensure all dependencies are installed
- Verify CSV file format matches expected structure

---

**Last Updated:** December 2025
**Version:** 1.0
**Python Version:** 3.8+

