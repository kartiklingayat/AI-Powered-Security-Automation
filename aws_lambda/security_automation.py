"""
AWS Lambda Handler for AI-Powered Security Automation
Main entry point for serverless security automation
"""

import json
import boto3
from threat_detection import ThreatDetector
from incident_response import IncidentResponder

# Initialize AWS clients
cloudwatch = boto3.client('cloudwatch')
sns = boto3.client('sns')

class SecurityAutomation:
    def __init__(self):
        self.threat_detector = ThreatDetector()
        self.incident_responder = IncidentResponder()
        
    def process_security_event(self, event):
        """
        Process security events from CloudTrail, VPC Flow Logs, etc.
        """
        print(f"[SECURITY] Processing {len(event.get('Records', []))} security events")
        
        threats_detected = []
        for record in event.get('Records', []):
            threat_analysis = self.threat_detector.analyze_event(record)
            
            if threat_analysis['is_threat']:
                threats_detected.append(threat_analysis)
                # Auto-remediate if threat is critical
                if threat_analysis['severity'] == 'CRITICAL':
                    self.incident_responder.auto_remediate(threat_analysis)
        
        return {
            'total_events': len(event.get('Records', [])),
            'threats_detected': len(threats_detected),
            'threat_details': threats_detected
        }

def lambda_handler(event, context):
    """
    AWS Lambda entry point for security automation
    """
    try:
        automation = SecurityAutomation()
        result = automation.process_security_event(event)
        
        # Log metrics to CloudWatch
        cloudwatch.put_metric_data(
            Namespace='SecurityAutomation',
            MetricData=[
                {
                    'MetricName': 'EventsProcessed',
                    'Value': result['total_events'],
                    'Unit': 'Count'
                },
                {
                    'MetricName': 'ThreatsDetected',
                    'Value': result['threats_detected'],
                    'Unit': 'Count'
                }
            ]
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Security automation completed successfully',
                'results': result
            })
        }
        
    except Exception as e:
        print(f"[ERROR] Security automation failed: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Security automation processing failed',
                'details': str(e)
            })
        }
