"""
Unit Tests for AI-Powered Security Automation
"""

import unittest
import json
from src.ml_analyzer import MLAnalyzer
from src.incident_response import IncidentResponder
from aws_lambda.threat_detection import ThreatDetector

class TestSecurityAutomation(unittest.TestCase):
    
    def setUp(self):
        self.ml_analyzer = MLAnalyzer()
        self.incident_responder = IncidentResponder()
        self.threat_detector = ThreatDetector()
        
    def test_threat_detection_malicious_ip(self):
        """Test detection of known malicious IP"""
        test_event = {
            'sourceIPAddress': '192.168.1.100',
            'eventName': 'ConsoleLogin',
            'userIdentity': {'userName': 'testuser'}
        }
        
        result = self.threat_detector.analyze_event(test_event)
        self.assertTrue(result['is_threat'])
        self.assertEqual(result['threat_type'], 'KNOWN_MALICIOUS_IP')
    
    def test_threat_detection_suspicious_activity(self):
        """Test detection of suspicious activity"""
        test_event = {
            'eventName': 'UnauthorizedAPICall',
            'errorCode': 'AccessDenied'
        }
        
        result = self.threat_detector.analyze_event(test_event)
        self.assertTrue(result['is_threat'])
        self.assertEqual(result['threat_type'], 'SUSPICIOUS_ACTIVITY')
    
    def test_ml_anomaly_detection(self):
        """Test ML-based anomaly detection"""
        # Training data
        training_data = [
            {'request_count': 100, 'error_rate': 0.01, 'response_time': 50, 'data_transfer': 1024},
            {'request_count': 150, 'error_rate': 0.02, 'response_time': 45, 'data_transfer': 2048},
        ]
        
        # Train model
        self.ml_analyzer.train_model(training_data)
        
        # Test normal data
        normal_data = {'request_count': 120, 'error_rate': 0.015, 'response_time': 55, 'data_transfer': 1536}
        result_normal = self.ml_analyzer.detect_anomalies(normal_data)
        self.assertFalse(result_normal['is_anomaly'])
        
        # Test anomalous data
        anomalous_data = {'request_count': 5000, 'error_rate': 0.5, 'response_time': 500, 'data_transfer': 1048576}
        result_anomaly = self.ml_analyzer.detect_anomalies(anomalous_data)
        self.assertTrue(result_anomaly['is_anomaly'])
    
    def test_incident_response(self):
        """Test automated incident response"""
        test_threat = {
            'threat_type': 'KNOWN_MALICIOUS_IP',
            'severity': 'HIGH',
            'event_details': {
                'sourceIPAddress': '192.168.1.100',
                'eventName': 'ConsoleLogin'
            }
        }
        
        result = self.incident_responder.auto_remediate(test_threat)
        self.assertEqual(result['threat_type'], 'KNOWN_MALICIOUS_IP')
        self.assertTrue(len(result['remediation_actions']) > 0)

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
