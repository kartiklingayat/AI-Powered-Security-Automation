"""
Threat Detection Module using ML-based anomaly detection
"""

import json
import re
from datetime import datetime, timedelta

class ThreatDetector:
    def __init__(self):
        # Known malicious patterns and IOCs
        self.malicious_ips = self._load_malicious_ips()
        self.suspicious_activities = [
            'unauthorized', 'brute force', 'port scanning',
            'data exfiltration', 'privilege escalation'
        ]
        
    def _load_malicious_ips(self):
        """Load known malicious IPs from threat intelligence"""
        return [
            '192.168.1.100',  # Example malicious IP
            '10.0.0.50'       # Example internal threat
        ]
    
    def analyze_event(self, event):
        """
        Analyze security event for potential threats using ML rules
        """
        event_str = json.dumps(event).lower()
        
        # Check for known threat patterns
        severity = 'LOW'
        threat_type = None
        confidence = 0.7
        
        # Pattern 1: Malicious IP detection
        for malicious_ip in self.malicious_ips:
            if malicious_ip in event_str:
                severity = 'HIGH'
                threat_type = 'KNOWN_MALICIOUS_IP'
                confidence = 0.9
                break
        
        # Pattern 2: Suspicious activity keywords
        for activity in self.suspicious_activities:
            if activity in event_str:
                if severity != 'HIGH':
                    severity = 'MEDIUM'
                threat_type = 'SUSPICIOUS_ACTIVITY'
                confidence = max(confidence, 0.8)
                break
        
        # Pattern 3: Unusual API calls
        if self._detect_unusual_api_calls(event):
            severity = 'MEDIUM'
            threat_type = 'UNUSUAL_API_ACTIVITY'
            confidence = 0.75
        
        # Pattern 4: High frequency events (DDoS pattern)
        if self._detect_high_frequency(event):
            severity = 'CRITICAL'
            threat_type = 'HIGH_FREQUENCY_ATTACK'
            confidence = 0.95
        
        return {
            'is_threat': threat_type is not None,
            'threat_type': threat_type,
            'severity': severity,
            'confidence': confidence,
            'timestamp': datetime.utcnow().isoformat(),
            'event_details': event
        }
    
    def _detect_unusual_api_calls(self, event):
        """Detect unusual API call patterns"""
        unusual_apis = ['DeleteBucket', 'StopLogging', 'DeleteTrail']
        event_str = json.dumps(event)
        return any(api in event_str for api in unusual_apis)
    
    def _detect_high_frequency(self, event):
        """Detect high frequency patterns (simplified)"""
        # In production, this would analyze event frequency over time
        return event.get('requestCount', 0) > 1000  # Example threshold
