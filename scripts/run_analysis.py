#!/usr/bin/env python3
"""
Water Quality Analysis - Complete Execution Script
Run all analysis steps from the notebook in a single script
"""

print("=" * 80)
print("WATER QUALITY CLASSIFICATION & PREDICTION SYSTEM")
print("=" * 80)
print()

# ============================================================================
# STEP 1: Import Libraries
# ============================================================================
print("📦 Step 1/11: Importing libraries...")

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score, 
    mean_squared_error, r2_score, mean_absolute_error
)
from sklearn.impute import SimpleImputer
import xgboost as xgb

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')
pd.set_option('display.max_columns', None)

print(f"✅ Libraries imported! TensorFlow: {tf.__version__}, Pandas: {pd.__version__}")
print()

# ============================================================================
# STEP 2: Load Data
# ============================================================================
print("📊 Step 2/11: Loading data...")

df = pd.read_csv('Water_Quality_Data_06_2025.csv')
print(f"✅ Loaded {df.shape[0]} rows × {df.shape[1]} columns")
print(f"   Monitoring Stations: {df['Station code'].nunique()}")
print(f"   Water Bodies: {df['water_bodies'].nunique()}")
print()

# ============================================================================
# STEP 3: Data Cleaning
# ============================================================================
print("🧹 Step 3/11: Cleaning data...")

df_clean = df.copy()

# Remove invalid samples
remarks_to_remove = ['dried up', 'lake emptied', 'under renovation', 'not collected', 
                     'No Access', 'lake covered', 'Lake covered']
initial_count = len(df_clean)
for remark in remarks_to_remove:
    df_clean = df_clean[~df_clean['Remarks'].astype(str).str.contains(remark, case=False, na=False)]

print(f"✅ Removed {initial_count - len(df_clean)} invalid samples")

# Select key parameters
key_parameters = [
    'DO (mg/L)', 'pH', 'Conductivity (mS/cm)', 'BOD (mg/L)', 'COD (mg/L)',
    'Nitrate', 'Nitrite-N (mg/L)', 'Fecal Coliform (MPN/100ml)', 
    'Total Coliform (MPN/100ml)', 'Turbidity (NTU)', 'Total Alk. (mg/L)',
    'Chloride (mg/L)', 'TDS (mg/L)', 'TSS (mg/L)', 'Total Phosphate (mg/L)',
    'Ammonia', 'Hardness (mg/L)', 'Fluoride (mg/L)'
]

metadata_cols = ['Station code', 'water_bodies', 'Station name']
cols_to_keep = metadata_cols + [col for col in key_parameters if col in df_clean.columns]
df_clean = df_clean[cols_to_keep]

# Convert to numeric
def clean_numeric_column(series):
    series = series.replace(['BDL', 'Less than 1.8', 'NIL', ''], np.nan)
    return pd.to_numeric(series, errors='coerce')

for col in key_parameters:
    if col in df_clean.columns:
        df_clean[col] = clean_numeric_column(df_clean[col])

# Remove rows with too many missing values
threshold = len(key_parameters) * 0.5
df_clean = df_clean.dropna(thresh=len(metadata_cols) + threshold)

print(f"✅ Cleaned data: {df_clean.shape[0]} samples × {df_clean.shape[1]} columns")
print()

# ============================================================================
# STEP 4: Calculate WQI
# ============================================================================
print("🔬 Step 4/11: Calculating Water Quality Index...")

# WHO/BIS Standards
standards = {
    'pH': {'ideal': 7.0, 'min': 6.5, 'max': 8.5, 'weight': 4},
    'DO (mg/L)': {'ideal': 6.0, 'min': 5.0, 'max': 14.0, 'weight': 5},
    'BOD (mg/L)': {'ideal': 0, 'min': 0, 'max': 3.0, 'weight': 5},
    'COD (mg/L)': {'ideal': 0, 'min': 0, 'max': 10.0, 'weight': 4},
    'Nitrate': {'ideal': 0, 'min': 0, 'max': 45.0, 'weight': 5},
    'Total Coliform (MPN/100ml)': {'ideal': 0, 'min': 0, 'max': 50, 'weight': 5},
    'Fecal Coliform (MPN/100ml)': {'ideal': 0, 'min': 0, 'max': 10, 'weight': 5},
    'TDS (mg/L)': {'ideal': 300, 'min': 0, 'max': 500, 'weight': 4},
    'Turbidity (NTU)': {'ideal': 1, 'min': 0, 'max': 5, 'weight': 3},
    'Chloride (mg/L)': {'ideal': 200, 'min': 0, 'max': 250, 'weight': 3},
    'Hardness (mg/L)': {'ideal': 100, 'min': 0, 'max': 300, 'weight': 2},
    'Fluoride (mg/L)': {'ideal': 1.0, 'min': 0.5, 'max': 1.5, 'weight': 4}
}

def calculate_qi(value, param_name, standards):
    if pd.isna(value) or param_name not in standards:
        return np.nan
    std = standards[param_name]
    
    if param_name == 'pH':
        if std['min'] <= value <= std['max']:
            qi = 100 - abs(value - std['ideal']) * 10
        else:
            qi = max(0, 100 - abs(value - std['ideal']) * 20)
    elif std['ideal'] == 0:
        if value <= std['max']:
            qi = 100 - (value / std['max']) * 100
        else:
            qi = max(0, 100 - (value / std['max']) * 150)
    else:
        if value <= std['max']:
            qi = 100 - abs(value - std['ideal']) / std['max'] * 100
        else:
            qi = max(0, 100 - (value - std['max']) / std['max'] * 100)
    return max(0, min(100, qi))

def calculate_wqi(row, standards):
    qi_values, weights = [], []
    for param, std_values in standards.items():
        if param in row.index:
            qi = calculate_qi(row[param], param, standards)
            if not pd.isna(qi):
                qi_values.append(qi)
                weights.append(std_values['weight'])
    if len(qi_values) == 0:
        return np.nan
    return sum(q * w for q, w in zip(qi_values, weights)) / sum(weights)

df_clean['WQI'] = df_clean.apply(lambda row: calculate_wqi(row, standards), axis=1)
print(f"✅ WQI calculated! Mean: {df_clean['WQI'].mean():.2f}, Median: {df_clean['WQI'].median():.2f}")
print()

# ============================================================================
# STEP 5: Create Classification Labels
# ============================================================================
print("🏷️  Step 5/11: Creating classification labels...")

def classify_water_quality(wqi):
    if pd.isna(wqi):
        return np.nan
    elif wqi >= 70:
        return 'Safe/Potable'
    elif wqi >= 40:
        return 'Polluted'
    else:
        return 'Highly Polluted'

df_clean['Water_Quality_Class'] = df_clean['WQI'].apply(classify_water_quality)
df_clean = df_clean.dropna(subset=['WQI', 'Water_Quality_Class'])

print("Distribution:")
for category, count in df_clean['Water_Quality_Class'].value_counts().items():
    pct = (count / len(df_clean)) * 100
    print(f"   {category:20s}: {count:3d} ({pct:5.1f}%)")
print()

# ============================================================================
# STEP 6: Feature Preparation
# ============================================================================
print("🔧 Step 6/11: Preparing features for ML...")

feature_columns = [col for col in key_parameters if col in df_clean.columns]
X = df_clean[feature_columns].copy()
y_class = df_clean['Water_Quality_Class'].copy()
y_wqi = df_clean['WQI'].copy()

# Impute missing values
imputer = SimpleImputer(strategy='median')
X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=X.columns, index=X.index)

# Encode labels
label_encoder = LabelEncoder()
y_class_encoded = label_encoder.fit_transform(y_class)

print(f"✅ Features: {len(feature_columns)}, Samples: {len(X_imputed)}")
print()

# ============================================================================
# STEP 7: Train-Test Split
# ============================================================================
print("✂️  Step 7/11: Splitting data...")

X_train_class, X_test_class, y_train_class, y_test_class = train_test_split(
    X_imputed, y_class_encoded, test_size=0.2, random_state=42, stratify=y_class_encoded)

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_imputed, y_wqi, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_class_scaled = scaler.fit_transform(X_train_class)
X_test_class_scaled = scaler.transform(X_test_class)
X_train_reg_scaled = scaler.fit_transform(X_train_reg)
X_test_reg_scaled = scaler.transform(X_test_reg)

print(f"✅ Training: {len(X_train_class)}, Testing: {len(X_test_class)}")
print()

# ============================================================================
# STEP 8: Train Random Forest Models
# ============================================================================
print("🌲 Step 8/11: Training Random Forest models...")

# Classifier
rf_classifier = RandomForestClassifier(
    n_estimators=200, max_depth=15, min_samples_split=5,
    min_samples_leaf=2, random_state=42, n_jobs=-1)
rf_classifier.fit(X_train_class_scaled, y_train_class)
y_pred_rf = rf_classifier.predict(X_test_class_scaled)
test_acc_rf = accuracy_score(y_test_class, y_pred_rf)

# Regressor
rf_regressor = RandomForestRegressor(
    n_estimators=200, max_depth=15, min_samples_split=5,
    min_samples_leaf=2, random_state=42, n_jobs=-1)
rf_regressor.fit(X_train_reg_scaled, y_train_reg)
y_pred_rf_reg = rf_regressor.predict(X_test_reg_scaled)
test_r2_rf = r2_score(y_test_reg, y_pred_rf_reg)
test_rmse_rf = np.sqrt(mean_squared_error(y_test_reg, y_pred_rf_reg))

print(f"✅ RF Classifier - Accuracy: {test_acc_rf:.4f}")
print(f"✅ RF Regressor  - R²: {test_r2_rf:.4f}, RMSE: {test_rmse_rf:.4f}")
print()

# ============================================================================
# STEP 9: Train XGBoost Models
# ============================================================================
print("🚀 Step 9/11: Training XGBoost models...")

# Classifier
xgb_classifier = xgb.XGBClassifier(
    n_estimators=200, max_depth=8, learning_rate=0.1,
    subsample=0.8, colsample_bytree=0.8, random_state=42)
xgb_classifier.fit(X_train_class_scaled, y_train_class)
y_pred_xgb = xgb_classifier.predict(X_test_class_scaled)
test_acc_xgb = accuracy_score(y_test_class, y_pred_xgb)

# Regressor
xgb_regressor = xgb.XGBRegressor(
    n_estimators=200, max_depth=8, learning_rate=0.1,
    subsample=0.8, colsample_bytree=0.8, random_state=42)
xgb_regressor.fit(X_train_reg_scaled, y_train_reg)
y_pred_xgb_reg = xgb_regressor.predict(X_test_reg_scaled)
test_r2_xgb = r2_score(y_test_reg, y_pred_xgb_reg)
test_rmse_xgb = np.sqrt(mean_squared_error(y_test_reg, y_pred_xgb_reg))

print(f"✅ XGB Classifier - Accuracy: {test_acc_xgb:.4f}")
print(f"✅ XGB Regressor  - R²: {test_r2_xgb:.4f}, RMSE: {test_rmse_xgb:.4f}")
print()

# ============================================================================
# STEP 10: Train Neural Network Models
# ============================================================================
print("🧠 Step 10/11: Training Neural Network models...")

# Classifier
nn_classifier = Sequential([
    Dense(128, activation='relu', input_shape=(X_train_class_scaled.shape[1],)),
    BatchNormalization(), Dropout(0.3),
    Dense(64, activation='relu'),
    BatchNormalization(), Dropout(0.3),
    Dense(32, activation='relu'),
    BatchNormalization(), Dropout(0.2),
    Dense(len(label_encoder.classes_), activation='softmax')
])
nn_classifier.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
nn_classifier.fit(X_train_class_scaled, y_train_class, validation_split=0.2,
                  epochs=100, batch_size=32,
                  callbacks=[EarlyStopping(patience=15, restore_best_weights=True)],
                  verbose=0)
_, test_acc_nn = nn_classifier.evaluate(X_test_class_scaled, y_test_class, verbose=0)

# Regressor
nn_regressor = Sequential([
    Dense(128, activation='relu', input_shape=(X_train_reg_scaled.shape[1],)),
    BatchNormalization(), Dropout(0.3),
    Dense(64, activation='relu'),
    BatchNormalization(), Dropout(0.3),
    Dense(32, activation='relu'),
    BatchNormalization(), Dropout(0.2),
    Dense(1)
])
nn_regressor.compile(optimizer='adam', loss='mse', metrics=['mae'])
nn_regressor.fit(X_train_reg_scaled, y_train_reg, validation_split=0.2,
                 epochs=100, batch_size=32,
                 callbacks=[EarlyStopping(patience=15, restore_best_weights=True)],
                 verbose=0)
y_pred_nn_reg = nn_regressor.predict(X_test_reg_scaled, verbose=0).flatten()
test_r2_nn = r2_score(y_test_reg, y_pred_nn_reg)
test_rmse_nn = np.sqrt(mean_squared_error(y_test_reg, y_pred_nn_reg))

print(f"✅ NN Classifier - Accuracy: {test_acc_nn:.4f}")
print(f"✅ NN Regressor  - R²: {test_r2_nn:.4f}, RMSE: {test_rmse_nn:.4f}")
print()

# ============================================================================
# STEP 11: Save Models
# ============================================================================
print("💾 Step 11/11: Saving models...")

import pickle
import os

os.makedirs('models', exist_ok=True)

# Save classifiers
with open('models/rf_classifier.pkl', 'wb') as f:
    pickle.dump(rf_classifier, f)
with open('models/xgb_classifier.pkl', 'wb') as f:
    pickle.dump(xgb_classifier, f)
nn_classifier.save('models/nn_classifier.keras')

# Save regressors
with open('models/rf_regressor.pkl', 'wb') as f:
    pickle.dump(rf_regressor, f)
with open('models/xgb_regressor.pkl', 'wb') as f:
    pickle.dump(xgb_regressor, f)
nn_regressor.save('models/nn_regressor.keras')

# Save preprocessors
with open('models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
with open('models/label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)
with open('models/imputer.pkl', 'wb') as f:
    pickle.dump(imputer, f)
with open('models/feature_names.pkl', 'wb') as f:
    pickle.dump(feature_columns, f)

print("✅ All models saved in 'models/' directory")
print()

# ============================================================================
# SUMMARY
# ============================================================================
print("=" * 80)
print("ANALYSIS COMPLETE! 🎉")
print("=" * 80)
print()
print("📊 MODEL PERFORMANCE SUMMARY:")
print()
print("Classification Models (Accuracy):")
print(f"   Random Forest:    {test_acc_rf:.4f}")
print(f"   XGBoost:          {test_acc_xgb:.4f}")
print(f"   Neural Network:   {test_acc_nn:.4f}")
print()
print("Regression Models (R² Score):")
print(f"   Random Forest:    {test_r2_rf:.4f} (RMSE: {test_rmse_rf:.2f})")
print(f"   XGBoost:          {test_r2_xgb:.4f} (RMSE: {test_rmse_xgb:.2f})")
print(f"   Neural Network:   {test_r2_nn:.4f} (RMSE: {test_rmse_nn:.2f})")
print()
print("🎯 Next Steps:")
print("   1. Run predictions: python3 predict_water_quality.py")
print("   2. Check saved models in 'models/' directory")
print("   3. Review visualizations in the notebook for detailed insights")
print()
print("=" * 80)

