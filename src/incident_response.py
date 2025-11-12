"""
Automated Incident Response Module
Handles automatic remediation and notification
"""

import boto3
import json
from datetime import datetime

class IncidentResponder:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.sns = boto3.client('sns')
        self.cloudwatch = boto3.client('cloudwatch')
        
    def auto_remediate(self, threat_analysis):
        """
        Automatically remediate threats based on severity and type
        """
        threat_type = threat_analysis['threat_type']
        severity = threat_analysis['severity']
        
        print(f"[RESPONSE] Auto-remediating threat: {threat_type} (Severity: {severity})")
        
        remediation_actions = []
        
        if threat_type == 'KNOWN_MALICIOUS_IP':
            remediation_actions.append(self._block_ip(threat_analysis))
            
        elif threat_type == 'HIGH_FREQUENCY_ATTACK':
            remediation_actions.append(self._trigger_ddos_protection())
            
        elif threat_type == 'UNUSUAL_API_ACTIVITY':
            remediation_actions.append(self._disable_compromised_user())
        
        # Send notification
        self._send_alert(threat_analysis, remediation_actions)
        
        return {
            'threat_type': threat_type,
            'severity': severity,
            'remediation_actions': remediation_actions,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _block_ip(self, threat_analysis):
        """Block malicious IP in security groups"""
        try:
            # Extract IP from event (simplified)
            event_details = threat_analysis['event_details']
            source_ip = event_details.get('sourceIPAddress', '0.0.0.0/32')
            
            # In production, this would update security groups
            print(f"[RESPONSE] Blocking IP: {source_ip}")
            
            return {
                'action': 'BLOCK_IP',
                'target': source_ip,
                'status': 'COMPLETED'
            }
        except Exception as e:
            return {
                'action': 'BLOCK_IP',
                'status': 'FAILED',
                'error': str(e)
            }
    
    def _trigger_ddos_protection(self):
        """Trigger DDoS protection mechanisms"""
        print("[RESPONSE] Activating DDoS protection protocols")
        
        return {
            'action': 'ACTIVATE_DDOS_PROTECTION',
            'status': 'COMPLETED'
        }
    
    def _disable_compromised_user(self):
        """Disable compromised IAM user"""
        print("[RESPONSE] Disabling compromised IAM user")
        
        return {
            'action': 'DISABLE_IAM_USER',
            'status': 'COMPLETED'
        }
    
    def _send_alert(self, threat_analysis, actions):
        """Send alert notification"""
        message = {
            'subject': f"🚨 SECURITY ALERT: {threat_analysis['threat_type']}",
            'body': {
                'threat_details': threat_analysis,
                'remediation_actions': actions,
                'timestamp': datetime.utcnow().isoformat()
            }
        }
        
        print(f"[ALERT] Security alert sent: {message['subject']}")
        
        # In production, this would send SNS notification
        # self.sns.publish(
        #     TopicArn='arn:aws:sns:region:account:security-alerts',
        #     Message=json.dumps(message['body']),
        #     Subject=message['subject']
        # )

# Example usage
if __name__ == "__main__":
    responder = IncidentResponder()
    
    # Test threat
    test_threat = {
        'threat_type': 'KNOWN_MALICIOUS_IP',
        'severity': 'HIGH',
        'event_details': {
            'sourceIPAddress': '192.168.1.100',
            'eventName': 'ConsoleLogin'
        }
    }
    
    result = responder.auto_remediate(test_threat)
    print(f"Remediation result: {result}")
