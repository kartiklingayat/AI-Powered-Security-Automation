"""
Machine Learning Analyzer for Advanced Threat Detection
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import json

class MLAnalyzer:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.features = ['request_count', 'error_rate', 'response_time', 'data_transfer']
        
    def train_model(self, training_data):
        """
        Train Isolation Forest model for anomaly detection
        """
        print("[ML] Training anomaly detection model...")
        
        # Prepare features
        df = pd.DataFrame(training_data)
        X = df[self.features]
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Isolation Forest
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.1,
            random_state=42
        )
        self.model.fit(X_scaled)
        
        print("[ML] Model training completed successfully")
        return self.model
    
    def detect_anomalies(self, real_time_data):
        """
        Detect anomalies in real-time security data
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_model first.")
        
        df = pd.DataFrame([real_time_data])
        X = df[self.features]
        X_scaled = self.scaler.transform(X)
        
        # Predict anomalies (-1 for anomalies, 1 for normal)
        predictions = self.model.predict(X_scaled)
        anomaly_scores = self.model.decision_function(X_scaled)
        
        is_anomaly = predictions[0] == -1
        confidence = abs(anomaly_scores[0])
        
        return {
            'is_anomaly': is_anomaly,
            'confidence': confidence,
            'anomaly_score': anomaly_scores[0],
            'features_analyzed': self.features
        }
    
    def save_model(self, filepath):
        """Save trained model to file"""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'features': self.features
        }, filepath)
        print(f"[ML] Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load trained model from file"""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.features = model_data['features']
        print(f"[ML] Model loaded from {filepath}")

# Example usage and testing
if __name__ == "__main__":
    # Sample training data
    training_data = [
        {'request_count': 100, 'error_rate': 0.01, 'response_time': 50, 'data_transfer': 1024},
        {'request_count': 150, 'error_rate': 0.02, 'response_time': 45, 'data_transfer': 2048},
        {'request_count': 5000, 'error_rate': 0.5, 'response_time': 500, 'data_transfer': 1048576},  # Anomaly
        {'request_count': 120, 'error_rate': 0.015, 'response_time': 55, 'data_transfer': 1536},
    ]
    
    # Initialize and train model
    ml_analyzer = MLAnalyzer()
    ml_analyzer.train_model(training_data)
    
    # Test with real-time data
    test_data = {'request_count': 6000, 'error_rate': 0.6, 'response_time': 600, 'data_transfer': 2097152}
    result = ml_analyzer.detect_anomalies(test_data)
    
    print(f"Anomaly Detection Result: {result}")
