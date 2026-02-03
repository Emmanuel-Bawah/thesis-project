#!/usr/bin/env python3
"""
Automated Testing with Adaptive Post-Quantum Selection
Tests adaptive system across multiple configurations
"""

import sys
import json
import time
import csv
from datetime import datetime
from pathlib import Path

sys.path.insert(0, '/home/ubuntu/thesis-project/src/adaptive')
sys.path.insert(0, '/home/ubuntu/thesis-project/scripts')

from adaptive_selector import AdaptivePostQuantumSelector
from device_simulator import DeviceSimulator

class AdaptiveTestHarness:
    def __init__(self):
        self.adaptive_selector = AdaptivePostQuantumSelector()
        
        self.device_types = ['low-end', 'mid-range', 'high-end']
        self.network_conditions = ['2G', '3G', '4G']
        self.transaction_amounts = [5.0, 25.0, 150.0]  # Low, Medium, High
        
        self.results_dir = Path.home() / 'thesis-project' / 'data' / 'results'
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        self.test_data_template = {
            'transaction_id': 'TXN_ADAPTIVE',
            'currency': 'USD',
            'merchant': 'MERCHANT_001',
            'customer_id': 'CUST_001',
            'payment_method': 'mobile_wallet',
            'country': 'GH'
        }
    
    def get_device_ram(self, device_type):
        """Get RAM for device type."""
        ram_map = {
            'low-end': 1536,    # 1.5GB
            'mid-range': 3584,  # 3.5GB
            'high-end': 7168    # 7GB
        }
        return ram_map[device_type]
    
    def run_adaptive_test(self, device_type, network_condition, transaction_amount, run_number):
        """Run single test with adaptive selection."""
        try:
            device_ram = self.get_device_ram(device_type)
            
            # Adaptive system selects algorithm
            algo_name, system, reason = self.adaptive_selector.select_algorithm(
                device_ram, network_condition, transaction_amount
            )
            
            # Create test data
            test_data = self.test_data_template.copy()
            test_data['amount'] = transaction_amount
            test_data['device_type'] = device_type
            test_data['timestamp'] = datetime.now().isoformat()
            plaintext = json.dumps(test_data).encode('utf-8')
            
            # Run encryption test
            start_time = time.time()
            public_key, private_key = system.generate_keypair()
            keygen_time = (time.time() - start_time) * 1000
            
            start_time = time.time()
            encrypted = system.encrypt(plaintext, public_key)
            encryption_time = (time.time() - start_time) * 1000
            
            start_time = time.time()
            decrypted = system.decrypt(encrypted, private_key)
            decryption_time = (time.time() - start_time) * 1000
            
            decrypted_data = json.loads(decrypted.decode('utf-8'))
            verified = (test_data == decrypted_data)
            
            return {
                'system': 'Adaptive',
                'selected_algorithm': algo_name,
                'selection_reason': reason[:100],  # Truncate for CSV
                'device_type': device_type,
                'device_ram_mb': device_ram,
                'network_condition': network_condition,
                'transaction_amount': transaction_amount,
                'run_number': run_number,
                'keygen_time_ms': keygen_time,
                'encryption_time_ms': encryption_time,
                'decryption_time_ms': decryption_time,
                'verified': verified,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'system': 'Adaptive',
                'device_type': device_type,
                'network_condition': network_condition,
                'transaction_amount': transaction_amount,
                'run_number': run_number,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def test_adaptive_system(self, runs_per_config=10):
        """Test adaptive system across all configurations."""
        print("\n" + "="*70)
        print("ADAPTIVE POST-QUANTUM SYSTEM TESTING")
        print("="*70)
        print(f"Devices: {len(self.device_types)} types")
        print(f"Networks: {len(self.network_conditions)} conditions")
        print(f"Amounts: {len(self.transaction_amounts)} values")
        print(f"Runs per config: {runs_per_config}")
        print(f"Total tests: {len(self.device_types) * len(self.network_conditions) * len(self.transaction_amounts) * runs_per_config}")
        print("="*70)
        
        all_results = []
        total_configs = len(self.device_types) * len(self.network_conditions) * len(self.transaction_amounts)
        config_count = 0
        
        start_time = datetime.now()
        
        for device in self.device_types:
            for network in self.network_conditions:
                for amount in self.transaction_amounts:
                    config_count += 1
                    print(f"\n[{config_count}/{total_configs}] {device} + {network} + ${amount:.0f}", end=' ')
                    
                    for run in range(1, runs_per_config + 1):
                        result = self.run_adaptive_test(device, network, amount, run)
                        all_results.append(result)
                        time.sleep(0.05)  # Small delay
                    
                    print("✓")
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("\n" + "="*70)
        print("ADAPTIVE TESTING COMPLETE")
        print("="*70)
        print(f"Total tests: {len(all_results)}")
        print(f"Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
        print("="*70)
        
        # Show selection statistics
        self.adaptive_selector.print_selection_summary()
        
        return all_results
    
    def save_results(self, results, filename):
        """Save results to CSV."""
        filepath = self.results_dir / filename
        
        if not results:
            print("No results to save!")
            return
        
        fieldnames = list(results[0].keys())
        
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        print(f"\n✓ Results saved: {filepath}")
        print(f"  Records: {len(results)}")
        print(f"  File size: {filepath.stat().st_size / 1024:.1f} KB")

def main():
    harness = AdaptiveTestHarness()
    
    print("\nAdaptive Post-Quantum Encryption Testing")
    print("This will test the adaptive system across:")
    print("  - 3 device types (low-end, mid-range, high-end)")
    print("  - 3 network conditions (2G, 3G, 4G)")
    print("  - 3 transaction amounts ($5, $25, $150)")
    print("  - 10 runs each")
    print("  = 270 tests total")
    print("\nEstimated time: 3-5 minutes")
    
    input("\nPress Enter to start testing...")
    
    results = harness.test_adaptive_system(runs_per_config=10)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    harness.save_results(results, f'adaptive_test_{timestamp}.csv')
    
    print("\n✓ Adaptive post-quantum testing complete!")

if __name__ == '__main__':
    main()
