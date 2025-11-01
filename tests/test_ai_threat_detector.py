#!/usr/bin/env python3
"""
Test script for AIThreatDetector module
Tests AI-powered threat detection and analysis functionality
"""

import asyncio
import sys
import os
import pytest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.defense.ai_threat_detector import get_ai_threat_detector
from models import SeverityLevel

@pytest.mark.asyncio
async def test_ai_threat_detector():
    """Test AI threat detector functionality"""
    print("=== Testing AI Threat Detector ===\n")
    
    detector = get_ai_threat_detector()
    
    # Test 1: Get initial threat status
    print("1. Initial Threat Status:")
    try:
        status = await detector.get_threat_status()
        print(f"   Total threats: {status['threat_status']['total_threats']}")
        print(f"   AI analysis enabled: {status['threat_status']['ai_analysis_enabled']}")
        print(f"   Auto response enabled: {status['threat_status']['auto_response_enabled']}")
        print(f"   Recent threats (24h): {status['threat_status']['recent_threats_24h']}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    # Test 2: Analyze logs with SSH brute force pattern
    print("2. Analyzing SSH Brute Force Logs:")
    try:
        ssh_logs = [
            "Failed password for root from 192.168.1.100 port 22 ssh2",
            "Failed password for admin from 192.168.1.100 port 22 ssh2",
            "Failed password for user from 192.168.1.100 port 22 ssh2",
            "Failed password for test from 192.168.1.100 port 22 ssh2",
            "Failed password for guest from 192.168.1.100 port 22 ssh2",
            "Failed password for oracle from 192.168.1.100 port 22 ssh2"
        ]
        
        result = await detector.analyze_logs(ssh_logs, "ssh_server")
        print(f"   Success: {result['success']}")
        print(f"   Log entries analyzed: {result['analysis_results']['log_entries_analyzed']}")
        print(f"   Threats detected: {result['analysis_results']['threats_detected']}")
        print(f"   Pattern threats: {result['analysis_results']['pattern_threats']}")
        print(f"   Analysis time: {result['analysis_results']['analysis_time_ms']:.2f}ms")
        
        if result['threats']:
            for threat in result['threats']:
                print(f"   - Threat: {threat['threat_type']} ({threat['severity']})")
                print(f"     Source IP: {threat['source_ip']}")
                print(f"     Description: {threat['description']}")
        
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    # Test 3: Analyze logs with SQL injection pattern
    print("3. Analyzing SQL Injection Logs:")
    try:
        sql_logs = [
            "GET /login.php?user=admin' UNION SELECT * FROM users-- HTTP/1.1",
            "POST /search.php - Query: ' OR 1=1; DROP TABLE users; --",
            "GET /products.php?id=1' AND 1=1 UNION SELECT password FROM admin--"
        ]
        
        result = await detector.analyze_logs(sql_logs, "web_server")
        print(f"   Success: {result['success']}")
        print(f"   Threats detected: {result['analysis_results']['threats_detected']}")
        
        if result['threats']:
            for threat in result['threats']:
                print(f"   - Threat: {threat['threat_type']} ({threat['severity']})")
                print(f"     Description: {threat['description']}")
                print(f"     Mitigation steps: {len(threat['mitigation_steps'])} steps")
        
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    # Test 4: Analyze logs with XSS pattern
    print("4. Analyzing XSS Attack Logs:")
    try:
        xss_logs = [
            "GET /comment.php?msg=<script>alert('XSS')</script> HTTP/1.1",
            "POST /feedback.php - Content: <img src=x onerror=alert(1)>",
            "GET /search.php?q=javascript:alert(document.cookie)"
        ]
        
        result = await detector.analyze_logs(xss_logs, "web_server")
        print(f"   Success: {result['success']}")
        print(f"   Threats detected: {result['analysis_results']['threats_detected']}")
        
        if result['threats']:
            for threat in result['threats']:
                print(f"   - Threat: {threat['threat_type']} ({threat['severity']})")
                print(f"     Indicators: {len(threat['indicators'])} found")
        
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    # Test 5: Analyze mixed logs for correlation
    print("5. Analyzing Mixed Logs for Correlation:")
    try:
        mixed_logs = [
            "Failed password for root from 10.0.0.50 port 22 ssh2",
            "Failed password for admin from 10.0.0.50 port 22 ssh2",
            "GET /admin.php?user=admin' UNION SELECT * FROM users-- from 10.0.0.50",
            "Connection attempt to port 80 from 10.0.0.50",
            "Connection attempt to port 443 from 10.0.0.50",
            "Connection attempt to port 21 from 10.0.0.50",
            "Failed password for user from 10.0.0.50 port 22 ssh2"
        ]
        
        result = await detector.analyze_logs(mixed_logs, "system")
        print(f"   Success: {result['success']}")
        print(f"   Threats detected: {result['analysis_results']['threats_detected']}")
        print(f"   Correlated threats: {result['analysis_results']['correlated_threats']}")
        
        if result['threats']:
            for threat in result['threats']:
                print(f"   - Threat: {threat['threat_type']} ({threat['severity']})")
                if threat['source_ip']:
                    print(f"     Source IP: {threat['source_ip']}")
        
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    # Test 6: List detected threats
    print("6. Listing All Detected Threats:")
    try:
        all_threats = detector.list_detected_threats()
        print(f"   Total threats detected: {len(all_threats)}")
        
        for threat in all_threats[:5]:  # Show first 5
            print(f"   - {threat['threat_id']}: {threat['threat_type']} ({threat['severity']})")
            print(f"     Detected: {threat['detected_at']}")
            print(f"     Resolved: {threat['resolved']}")
        
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    # Test 7: Filter threats by severity
    print("7. Filtering Critical Threats:")
    try:
        critical_threats = detector.list_detected_threats(SeverityLevel.CRITICAL)
        print(f"   Critical threats: {len(critical_threats)}")
        
        for threat in critical_threats:
            print(f"   - {threat['threat_type']}: {threat['description']}")
        
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    # Test 8: Resolve a threat
    print("8. Resolving Threats:")
    try:
        all_threats = detector.list_detected_threats()
        if all_threats:
            threat_to_resolve = all_threats[0]
            threat_id = threat_to_resolve['threat_id']
            
            result = await detector.resolve_threat(threat_id)
            print(f"   Success: {result['success']}")
            print(f"   Message: {result['message']}")
            print(f"   Resolved threat type: {result['threat_info']['threat_type']}")
        else:
            print("   No threats to resolve")
        
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    # Test 9: Final threat status
    print("9. Final Threat Status:")
    try:
        status = await detector.get_threat_status()
        print(f"   Total threats: {status['threat_status']['total_threats']}")
        print(f"   Severity distribution:")
        for severity, count in status['threat_status']['severity_distribution'].items():
            if count > 0:
                print(f"     {severity.upper()}: {count}")
        
        print(f"   Threat types:")
        for threat_type, count in status['threat_status']['threat_types'].items():
            print(f"     {threat_type}: {count}")
        
        if status['top_attacking_ips']:
            print(f"   Top attacking IPs:")
            for ip_info in status['top_attacking_ips'][:3]:
                print(f"     {ip_info['ip']}: {ip_info['threat_count']} threats")
        
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    print("=== AI Threat Detector Tests Completed ===")

if __name__ == "__main__":
    asyncio.run(test_ai_threat_detector())