#!/usr/bin/env python3
"""
Automated Testing Harness
MSC Thesis: Comprehensive Performance Testing Framework
"""

import sys
import os
import json
import time
import csv
from datetime import datetime
from pathlib import Path

sys.path.insert(0, '/home/ubuntu/thesis-project/src/kyber768')
sys.path.insert(0, '/home/ubuntu/thesis-project/src/rsa2048')
sys.path.insert(0, '/home/ubuntu/thesis-project/src/ecdh')
sys.path.insert(0, '/home/ubuntu/thesis-project/src/kyber512')
sys.path.insert(0, '/home/ubuntu/thesis-project/scripts')

from device_simulator import DeviceSimulator

class TestHarness:
    def __init__(self):
        self.systems = {
            'kyber768': {'name': 'Kyber-768', 'module': 'kyber768_system', 'class': 'Kyber768HybridEncryption'},
            'rsa2048': {'name': 'RSA-2048', 'module': 'rsa2048_baseline', 'class': 'RSA2048Baseline'},
            'ecdh': {'name': 'ECDH-P256', 'module': 'ecdh_baseline', 'class': 'ECDHBaseline'},
            'kyber512': {'name': 'Kyber-512', 'module': 'kyber512_baseline', 'class': 'Kyber512Baseline'}
        }
        
        self.device_types = ['low-end', 'mid-range', 'high-end']
        self.network_conditions = ['2G', '3G', '4G']
        
        self.results_dir = Path.home() / 'thesis-project' / 'data' / 'results'
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        self.test_data = {
            'transaction_id': 'TXN00000001',
            'amount': 125.50,
            'currency': 'USD',
            'merchant': 'ELEC1234',
            'customer_id': 'CUST5678',
            'timestamp': datetime.now().isoformat(),
            'payment_method': 'mobile_wallet',
            'device_type': 'mid-range',
            'country': 'GH'
        }
        self.plaintext = json.dumps(self.test_data).encode('utf-8')
    
    def load_system(self, system_key):
        system_info = self.systems[system_key]
        module = __import__(system_info['module'])
        crypto_class = getattr(module, system_info['class'])
        return crypto_class()
    
    def run_single_test(self, system_key, device_type, network_condition, run_number):
        try:
            crypto = self.load_system(system_key)
            device_profile = DeviceSimulator.get_profile(device_type)
            
            start_time = time.time()
            public_key, private_key = crypto.generate_keypair()
            keygen_time = (time.time() - start_time) * 1000
            
            start_time = time.time()
            encrypted = crypto.encrypt(self.plaintext, public_key)
            encryption_time = (time.time() - start_time) * 1000
            
            start_time = time.time()
            decrypted = crypto.decrypt(encrypted, private_key)
            decryption_time = (time.time() - start_time) * 1000
            
            decrypted_data = json.loads(decrypted.decode('utf-8'))
            verified = (self.test_data == decrypted_data)
            
            return {
                'system': self.systems[system_key]['name'],
                'device_type': device_type,
                'network_condition': network_condition,
                'run_number': run_number,
                'keygen_time_ms': keygen_time,
                'encryption_time_ms': encryption_time,
                'decryption_time_ms': decryption_time,
                'verified': verified,
                'timestamp': datetime.now().isoformat(),
                'public_key_size': len(public_key),
                'private_key_size': len(private_key)
            }
        except Exception as e:
            return {
                'system': self.systems[system_key]['name'],
                'device_type': device_type,
                'network_condition': network_condition,
                'run_number': run_number,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def run_test_batch(self, system_key, device_type, network_condition, num_runs=30):
        system_name = self.systems[system_key]['name']
        print(f"\nTesting {system_name} | {device_type} | {network_condition} | {num_runs} runs")
        
        results = []
        for run in range(1, num_runs + 1):
            if run % 10 == 0:
                print(f"  Progress: {run}/{num_runs}...")
            result = self.run_single_test(system_key, device_type, network_condition, run)
            results.append(result)
            time.sleep(0.05)
        
        print(f"  ✓ Completed {num_runs} runs")
        return results
    
    def quick_test(self):
        print("\n" + "="*70)
        print("QUICK TEST (3 runs per system, mid-range, 4G)")
        print("="*70)
        
        all_results = []
        for system_key in self.systems.keys():
            results = self.run_test_batch(system_key, 'mid-range', '4G', num_runs=3)
            all_results.extend(results)
        
        return all_results
    
    def standard_test(self, num_runs=30):
        """Standard test: all 4 systems, mid-range device, 4G network"""
        print("\n" + "="*70)
        print(f"STANDARD TEST ({num_runs} runs per system)")
        print("Configuration: mid-range device, 4G network")
        print("="*70)
        
        all_results = []
        start_time = datetime.now()
        
        for system_key in self.systems.keys():
            results = self.run_test_batch(system_key, 'mid-range', '4G', num_runs)
            all_results.extend(results)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("\n" + "="*70)
        print("STANDARD TEST COMPLETE")
        print("="*70)
        print(f"Total tests: {len(all_results)}")
        print(f"Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
        print("="*70)
        
        return all_results
    
    def save_results(self, results, filename='test_results.csv'):
        filepath = self.results_dir / filename
        
        if not results:
            print("No results to save!")
            return
        
        fieldnames = list(results[0].keys())
        
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        print(f"\n✓ Results saved to: {filepath}")
        print(f"  Records: {len(results)}")
        print(f"  File size: {filepath.stat().st_size / 1024:.1f} KB")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Automated Testing')
    parser.add_argument('--quick', action='store_true', help='Quick test (3 runs)')
    parser.add_argument('--runs', type=int, default=30, help='Runs per config')
    
    args = parser.parse_args()
    
    harness = TestHarness()
    
    if args.quick:
        results = harness.quick_test()
        harness.save_results(results, 'quick_test.csv')
    else:
        results = harness.standard_test(args.runs)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        harness.save_results(results, f'standard_test_{timestamp}.csv')
    
    print("\n✓ Testing complete!")

if __name__ == '__main__':
    main()
