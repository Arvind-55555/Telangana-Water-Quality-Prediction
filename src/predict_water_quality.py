#!/usr/bin/env python3
"""
Water Quality Prediction Script
Use trained models to predict water quality for new samples
"""

import pickle
import numpy as np
import pandas as pd
from tensorflow import keras

class WaterQualityPredictor:
    """Predict water quality using trained models"""
    
    def __init__(self, models_dir='models'):
        """Load trained models and preprocessors"""
        self.models_dir = models_dir
        
        # Load preprocessors
        with open(f'{models_dir}/scaler.pkl', 'rb') as f:
            self.scaler = pickle.load(f)
        with open(f'{models_dir}/label_encoder.pkl', 'rb') as f:
            self.label_encoder = pickle.load(f)
        with open(f'{models_dir}/imputer.pkl', 'rb') as f:
            self.imputer = pickle.load(f)
        with open(f'{models_dir}/feature_names.pkl', 'rb') as f:
            self.feature_names = pickle.load(f)
        
        # Load models
        with open(f'{models_dir}/rf_classifier.pkl', 'rb') as f:
            self.rf_classifier = pickle.load(f)
        with open(f'{models_dir}/xgb_classifier.pkl', 'rb') as f:
            self.xgb_classifier = pickle.load(f)
        self.nn_classifier = keras.models.load_model(f'{models_dir}/nn_classifier.keras')
        
        with open(f'{models_dir}/rf_regressor.pkl', 'rb') as f:
            self.rf_regressor = pickle.load(f)
        with open(f'{models_dir}/xgb_regressor.pkl', 'rb') as f:
            self.xgb_regressor = pickle.load(f)
        self.nn_regressor = keras.models.load_model(f'{models_dir}/nn_regressor.keras')
        
        print("✅ All models loaded successfully!")
    
    def preprocess_data(self, data):
        """Preprocess input data"""
        # Ensure we have all required features
        df = pd.DataFrame([data]) if isinstance(data, dict) else data
        
        # Select only feature columns
        df = df[self.feature_names]
        
        # Impute missing values
        df_imputed = pd.DataFrame(
            self.imputer.transform(df),
            columns=self.feature_names
        )
        
        # Scale features
        df_scaled = self.scaler.transform(df_imputed)
        
        return df_scaled
    
    def predict_class(self, data, model='rf'):
        """
        Predict water quality classification
        
        Parameters:
        -----------
        data : dict or pd.DataFrame
            Water quality parameters
        model : str
            Model to use: 'rf', 'xgb', or 'nn'
        
        Returns:
        --------
        str : Predicted class (Safe/Potable, Polluted, or Highly Polluted)
        """
        X = self.preprocess_data(data)
        
        if model == 'rf':
            pred = self.rf_classifier.predict(X)[0]
        elif model == 'xgb':
            pred = self.xgb_classifier.predict(X)[0]
        elif model == 'nn':
            pred = np.argmax(self.nn_classifier.predict(X, verbose=0), axis=1)[0]
        else:
            raise ValueError("Model must be 'rf', 'xgb', or 'nn'")
        
        return self.label_encoder.inverse_transform([pred])[0]
    
    def predict_wqi(self, data, model='rf'):
        """
        Predict Water Quality Index
        
        Parameters:
        -----------
        data : dict or pd.DataFrame
            Water quality parameters
        model : str
            Model to use: 'rf', 'xgb', or 'nn'
        
        Returns:
        --------
        float : Predicted WQI value
        """
        X = self.preprocess_data(data)
        
        if model == 'rf':
            wqi = self.rf_regressor.predict(X)[0]
        elif model == 'xgb':
            wqi = self.xgb_regressor.predict(X)[0]
        elif model == 'nn':
            wqi = self.nn_regressor.predict(X, verbose=0)[0][0]
        else:
            raise ValueError("Model must be 'rf', 'xgb', or 'nn'")
        
        return float(wqi)
    
    def predict_all(self, data):
        """
        Get predictions from all models
        
        Returns:
        --------
        dict : Predictions from all models
        """
        results = {
            'Classification': {
                'Random Forest': self.predict_class(data, 'rf'),
                'XGBoost': self.predict_class(data, 'xgb'),
                'Neural Network': self.predict_class(data, 'nn')
            },
            'WQI Prediction': {
                'Random Forest': round(self.predict_wqi(data, 'rf'), 2),
                'XGBoost': round(self.predict_wqi(data, 'xgb'), 2),
                'Neural Network': round(self.predict_wqi(data, 'nn'), 2)
            }
        }
        
        return results


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("WATER QUALITY PREDICTION SYSTEM")
    print("=" * 80)
    
    # Example water sample data
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
    
    print("\n📊 Sample Water Quality Data:")
    for param, value in sample_data.items():
        print(f"   {param}: {value}")
    
    print("\n🔄 Loading models and making predictions...\n")
    
    try:
        # Initialize predictor
        predictor = WaterQualityPredictor()
        
        # Get predictions
        results = predictor.predict_all(sample_data)
        
        print("\n" + "=" * 80)
        print("PREDICTION RESULTS")
        print("=" * 80)
        
        print("\n📋 Water Quality Classification:")
        for model, prediction in results['Classification'].items():
            print(f"   {model:20s}: {prediction}")
        
        print("\n📊 Water Quality Index (WQI) Prediction:")
        for model, wqi in results['WQI Prediction'].items():
            print(f"   {model:20s}: {wqi:.2f}")
        
        # Average predictions
        avg_wqi = sum(results['WQI Prediction'].values()) / len(results['WQI Prediction'])
        print(f"\n   Average WQI: {avg_wqi:.2f}")
        
        # Interpretation
        print("\n" + "=" * 80)
        print("INTERPRETATION")
        print("=" * 80)
        if avg_wqi >= 70:
            print("✅ Water Quality: SAFE/POTABLE")
            print("   The water meets quality standards for drinking/domestic use.")
        elif avg_wqi >= 40:
            print("⚠️  Water Quality: POLLUTED")
            print("   The water shows moderate pollution. Treatment recommended.")
        else:
            print("❌ Water Quality: HIGHLY POLLUTED")
            print("   The water is severely polluted. Not suitable for use.")
        
        print("=" * 80)
        
    except FileNotFoundError:
        print("\n❌ Error: Models not found!")
        print("Please run the Jupyter notebook first to train and save the models.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

