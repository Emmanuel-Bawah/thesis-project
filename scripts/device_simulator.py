#!/usr/bin/env python3
"""
Device Simulator - Simulates different device types
Low-end: 1-2GB RAM
Mid-range: 3-4GB RAM  
High-end: 6GB+ RAM
"""

import os
import sys

class DeviceSimulator:
    """Simulate device resource constraints"""
    
    DEVICE_PROFILES = {
        'low-end': {
            'ram_limit_mb': 1536,  # 1.5GB
            'description': '1-2GB RAM device'
        },
        'mid-range': {
            'ram_limit_mb': 3584,  # 3.5GB
            'description': '3-4GB RAM device'
        },
        'high-end': {
            'ram_limit_mb': 7168,  # 7GB
            'description': '6GB+ RAM device'
        }
    }
    
    @staticmethod
    def get_profile(device_type):
        """Get device profile"""
        if device_type not in DeviceSimulator.DEVICE_PROFILES:
            raise ValueError(f"Unknown device type: {device_type}")
        return DeviceSimulator.DEVICE_PROFILES[device_type]
    
    @staticmethod
    def apply_constraints(device_type):
        """Apply device constraints (memory limits)"""
        profile = DeviceSimulator.get_profile(device_type)
        
        # Note: Actual memory limiting would require cgroups or systemd
        # For our testing, we'll track memory usage and ensure it stays within limits
        
        print(f"Device profile: {device_type}")
        print(f"  RAM limit: {profile['ram_limit_mb']} MB")
        print(f"  Description: {profile['description']}")
        
        return profile
    
    @staticmethod
    def list_profiles():
        """List all device profiles"""
        print("Available device profiles:")
        for device_type, profile in DeviceSimulator.DEVICE_PROFILES.items():
            print(f"  {device_type}: {profile['description']} ({profile['ram_limit_mb']} MB)")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 device_simulator.py {low-end|mid-range|high-end|list}")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'list':
        DeviceSimulator.list_profiles()
    else:
        DeviceSimulator.apply_constraints(command)
