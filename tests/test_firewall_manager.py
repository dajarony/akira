#!/usr/bin/env python3
"""
Test script for FirewallManager module
Tests firewall rule management and IP blocking functionality
"""

import asyncio
import sys
import os
import pytest
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.defense.firewall_manager import get_firewall_manager
from models import FirewallRule, SeverityLevel

@pytest.mark.asyncio
async def test_firewall_manager():
    """Test firewall manager functionality"""
    print("=== Testing Firewall Manager ===\n")
    
    manager = get_firewall_manager()
    
    # Test 1: Get initial firewall status
    print("1. Initial Firewall Status:")
    try:
        status = await manager.get_firewall_status()
        print(f"   System type: {status['firewall_status']['system_type']}")
        print(f"   Total rules: {status['firewall_status']['total_rules']}")
        print(f"   Blocked IPs: {status['firewall_status']['blocked_ips_count']}")
        print(f"   Max rules: {status['firewall_status']['max_rules']}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    # Test 2: Create firewall rule
    print("2. Creating Firewall Rule:")
    try:
        test_rule = FirewallRule(
            rule_id="test_rule_001",
            rule_name="Test Block Rule",
            action="deny",
            source_ip="192.168.1.100",
            destination_port="80",
            protocol="tcp",
            enabled=True,
            expires_at=datetime.utcnow() + timedelta(hours=1)
        )
        
        result = await manager.create_firewall_rule(test_rule)
        print(f"   Success: {result['success']}")
        print(f"   Message: {result['message']}")
        print(f"   Rule ID: {result['rule_id']}")
        print(f"   Active rules count: {result['active_rules_count']}")
        
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    # Test 3: Block malicious IP
    print("3. Blocking Malicious IP:")
    try:
        result = await manager.block_malicious_ip(
            ip_address="10.0.0.50",
            threat_level=SeverityLevel.HIGH,
            duration_hours=2
        )
        
        print(f"   Success: {result['success']}")
        print(f"   Message: {result['message']}")
        print(f"   Rule ID: {result['rule_id']}")
        print(f"   Expires at: {result['expires_at']}")
        print(f"   Blocked IPs count: {result['blocked_ips_count']}")
        
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    # Test 4: List active rules
    print("4. Active Firewall Rules:")
    try:
        rules = manager.list_active_rules()
        print(f"   Total active rules: {len(rules)}")
        for rule in rules[:3]:  # Show first 3 rules
            print(f"   - {rule['rule_name']}: {rule['action']} {rule['source_ip'] or 'any'}")
        
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    # Test 5: Get blocked IPs
    print("5. Blocked IPs:")
    try:
        blocked_ips = manager.get_blocked_ips()
        print(f"   Total blocked IPs: {len(blocked_ips)}")
        for ip_info in blocked_ips[:3]:  # Show first 3 IPs
            print(f"   - {ip_info['ip_address']}: {ip_info['threat_level']} (attacks: {ip_info['attack_count']})")
        
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    # Test 6: Bulk block IPs
    print("6. Bulk Block IPs:")
    try:
        test_ips = ["172.16.0.10", "172.16.0.11", "172.16.0.12"]
        result = await manager.bulk_block_ips(test_ips, SeverityLevel.MEDIUM)
        
        print(f"   Success: {result['success']}")
        print(f"   Message: {result['message']}")
        print(f"   Blocked count: {result['blocked_count']}")
        print(f"   Failed count: {result['failed_count']}")
        
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    # Test 7: Unblock IP
    print("7. Unblocking IP:")
    try:
        result = await manager.unblock_ip("10.0.0.50")
        print(f"   Success: {result['success']}")
        print(f"   Message: {result['message']}")
        print(f"   Rules deleted: {result['rules_deleted']}")
        
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    # Test 8: Final firewall status
    print("8. Final Firewall Status:")
    try:
        status = await manager.get_firewall_status()
        print(f"   Total rules: {status['firewall_status']['total_rules']}")
        print(f"   Allow rules: {status['firewall_status']['allow_rules']}")
        print(f"   Deny rules: {status['firewall_status']['deny_rules']}")
        print(f"   Blocked IPs: {status['firewall_status']['blocked_ips_count']}")
        
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    print("=== Firewall Manager Tests Completed ===")

if __name__ == "__main__":
    asyncio.run(test_firewall_manager())