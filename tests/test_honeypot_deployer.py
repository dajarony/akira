#!/usr/bin/env python3
"""
Test script for HoneypotDeployer module
Tests honeypot deployment and management functionality
"""

import asyncio
import sys
import os
import time
import pytest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.defense.honeypot_deployer import get_honeypot_deployer

@pytest.mark.asyncio
async def test_honeypot_deployer():
    """Test honeypot deployer functionality"""
    print("=== Testing Honeypot Deployer ===\n")
    
    deployer = get_honeypot_deployer()
    
    # Test 1: Get initial honeypot status
    print("1. Initial Honeypot Status:")
    try:
        status = await deployer.get_honeypot_status()
        print(f"   Total honeypots: {status['honeypot_status']['total_honeypots']}")
        print(f"   Active honeypots: {status['honeypot_status']['active_honeypots']}")
        print(f"   Total connections: {status['honeypot_status']['total_connections_received']}")
        print(f"   Credentials captured: {status['honeypot_status']['total_credentials_captured']}")
        print(f"   Auto-block attackers: {status['honeypot_status']['auto_block_attackers']}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    # Test 2: Deploy SSH honeypot
    print("2. Deploying SSH Honeypot:")
    try:
        result = await deployer.deploy_ssh_honeypot(port=2222, interface="127.0.0.1")
        print(f"   Success: {result['success']}")
        print(f"   Message: {result['message']}")
        print(f"   Honeypot ID: {result['honeypot_id']}")
        print(f"   Port: {result['honeypot_info']['port']}")
        print(f"   Status: {result['honeypot_info']['status']}")
        
        ssh_honeypot_id = result['honeypot_id']
        
    except Exception as e:
        print(f"   Error: {str(e)}")
        ssh_honeypot_id = None
    print()
    
    # Test 3: Deploy HTTP honeypot
    print("3. Deploying HTTP Honeypot:")
    try:
        result = await deployer.deploy_http_honeypot(port=8080, interface="127.0.0.1")
        print(f"   Success: {result['success']}")
        print(f"   Message: {result['message']}")
        print(f"   Honeypot ID: {result['honeypot_id']}")
        print(f"   Port: {result['honeypot_info']['port']}")
        print(f"   Status: {result['honeypot_info']['status']}")
        
        http_honeypot_id = result['honeypot_id']
        
    except Exception as e:
        print(f"   Error: {str(e)}")
        http_honeypot_id = None
    print()
    
    # Test 4: Deploy FTP honeypot
    print("4. Deploying FTP Honeypot:")
    try:
        result = await deployer.deploy_ftp_honeypot(port=2121, interface="127.0.0.1")
        print(f"   Success: {result['success']}")
        print(f"   Message: {result['message']}")
        print(f"   Honeypot ID: {result['honeypot_id']}")
        print(f"   Port: {result['honeypot_info']['port']}")
        print(f"   Status: {result['honeypot_info']['status']}")
        
        ftp_honeypot_id = result['honeypot_id']
        
    except Exception as e:
        print(f"   Error: {str(e)}")
        ftp_honeypot_id = None
    print()
    
    # Test 5: List active honeypots
    print("5. Active Honeypots:")
    try:
        active_honeypots = deployer.list_active_honeypots()
        print(f"   Total active: {len(active_honeypots)}")
        for honeypot in active_honeypots:
            print(f"   - {honeypot['honeypot_name']}: {honeypot['honeypot_type']} on port {honeypot['port']}")
            print(f"     Connections: {honeypot['connections_received']}, Credentials: {honeypot['credentials_captured']}")
        
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    # Test 6: Wait a moment for potential connections (simulation)
    print("6. Waiting for potential connections (5 seconds)...")
    await asyncio.sleep(5)
    print("   Monitoring period completed")
    print()
    
    # Test 7: Get updated honeypot status
    print("7. Updated Honeypot Status:")
    try:
        status = await deployer.get_honeypot_status()
        print(f"   Total honeypots: {status['honeypot_status']['total_honeypots']}")
        print(f"   Active honeypots: {status['honeypot_status']['active_honeypots']}")
        print(f"   Total connections: {status['honeypot_status']['total_connections_received']}")
        print(f"   Credentials captured: {status['honeypot_status']['total_credentials_captured']}")
        
        # Show stats by type
        if status['stats_by_type']:
            print("   Stats by type:")
            for honeypot_type, stats in status['stats_by_type'].items():
                print(f"     {honeypot_type}: {stats['count']} honeypots, {stats['connections']} connections")
        
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    # Test 8: Stop individual honeypots
    print("8. Stopping Individual Honeypots:")
    
    if ssh_honeypot_id:
        try:
            result = await deployer.stop_honeypot(ssh_honeypot_id)
            print(f"   SSH Honeypot - Success: {result['success']}")
            print(f"   SSH Honeypot - Message: {result['message']}")
            print(f"   SSH Honeypot - Final connections: {result['final_stats']['connections_received']}")
        except Exception as e:
            print(f"   SSH Honeypot - Error: {str(e)}")
    
    if http_honeypot_id:
        try:
            result = await deployer.stop_honeypot(http_honeypot_id)
            print(f"   HTTP Honeypot - Success: {result['success']}")
            print(f"   HTTP Honeypot - Message: {result['message']}")
        except Exception as e:
            print(f"   HTTP Honeypot - Error: {str(e)}")
    
    print()
    
    # Test 9: Stop all remaining honeypots
    print("9. Stopping All Remaining Honeypots:")
    try:
        result = await deployer.stop_all_honeypots()
        print(f"   Success: {result['success']}")
        print(f"   Message: {result['message']}")
        print(f"   Stopped count: {result['stopped_count']}")
        print(f"   Failed count: {result['failed_count']}")
        
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    # Test 10: Final status check
    print("10. Final Honeypot Status:")
    try:
        status = await deployer.get_honeypot_status()
        print(f"    Total honeypots: {status['honeypot_status']['total_honeypots']}")
        print(f"    Active honeypots: {status['honeypot_status']['active_honeypots']}")
        print(f"    Total connections received: {status['honeypot_status']['total_connections_received']}")
        print(f"    Total credentials captured: {status['honeypot_status']['total_credentials_captured']}")
        
    except Exception as e:
        print(f"   Error: {str(e)}")
    print()
    
    print("=== Honeypot Deployer Tests Completed ===")

if __name__ == "__main__":
    asyncio.run(test_honeypot_deployer())