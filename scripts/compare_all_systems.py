#!/usr/bin/env python3
"""
Compare All 4 Encryption Systems
MSC Thesis: Performance Comparison on ARM64
"""

import sys
import json
from datetime import datetime

# Add src directories to path
sys.path.insert(0, '/home/ubuntu/thesis-project/src/kyber768')
sys.path.insert(0, '/home/ubuntu/thesis-project/src/rsa2048')
sys.path.insert(0, '/home/ubuntu/thesis-project/src/ecdh')
sys.path.insert(0, '/home/ubuntu/thesis-project/src/kyber512')

print("\n" + "=" * 70)
print("COMPREHENSIVE SYSTEM COMPARISON")
print("MSC Thesis: Post-Quantum E-Commerce Encryption on ARM")
print("Architecture: AWS t4g.micro (ARM64)")
print("=" * 70)

# Test transaction
transaction = {
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
plaintext = json.dumps(transaction).encode('utf-8')

results = []

# Test each system
systems = [
    ('Kyber-768 (Proposed)', 'kyber768_system', 'Kyber768HybridEncryption'),
    ('RSA-2048', 'rsa2048_baseline', 'RSA2048Baseline'),
    ('ECDH-P256', 'ecdh_baseline', 'ECDHBaseline'),
    ('Kyber-512', 'kyber512_baseline', 'Kyber512Baseline'),
]

for name, module_name, class_name in systems:
    print(f"\n{'=' * 70}")
    print(f"Testing: {name}")
    print('=' * 70)
    
    try:
        module = __import__(module_name)
        crypto_class = getattr(module, class_name)
        crypto = crypto_class()
        
        # Generate keypair
        public_key, private_key = crypto.generate_keypair()
        
        # Encrypt
        encrypted = crypto.encrypt(plaintext, public_key)
        
        # Decrypt
        decrypted = crypto.decrypt(encrypted, private_key)
        
        # Verify
        decrypted_data = json.loads(decrypted.decode('utf-8'))
        verified = (transaction == decrypted_data)
        
        # Get metrics
        metrics = crypto.get_performance_metrics()
        
        results.append({
            'system': name,
            'key_gen_ms': metrics['key_generation']['mean'],
            'encryption_ms': metrics['encryption']['mean'],
            'decryption_ms': metrics['decryption']['mean'],
            'verified': verified
        })
        
        print(f"✓ {name} test complete")
        
    except Exception as e:
        print(f"✗ Error testing {name}: {e}")
        results.append({
            'system': name,
            'error': str(e)
        })

# Print comparison table
print("\n" + "=" * 70)
print("PERFORMANCE COMPARISON TABLE")
print("=" * 70)
print(f"{'System':<25} {'KeyGen (ms)':<15} {'Encrypt (ms)':<15} {'Decrypt (ms)':<15}")
print("-" * 70)

for result in results:
    if 'error' not in result:
        print(f"{result['system']:<25} "
              f"{result['key_gen_ms']:<15.2f} "
              f"{result['encryption_ms']:<15.2f} "
              f"{result['decryption_ms']:<15.2f}")

print("=" * 70)

# Analysis
print("\n" + "=" * 70)
print("ANALYSIS")
print("=" * 70)

kyber768 = results[0]
rsa2048 = results[1]
ecdh = results[2]

print(f"\nKyber-768 vs RSA-2048:")
print(f"  Key Gen: {rsa2048['key_gen_ms']/kyber768['key_gen_ms']:.1f}x faster")
print(f"  Encryption: {rsa2048['encryption_ms']/kyber768['encryption_ms']:.2f}x")
print(f"  Decryption: {rsa2048['decryption_ms']/kyber768['decryption_ms']:.1f}x faster")

print(f"\nKyber-768 vs ECDH-P256:")
print(f"  Key Gen: {ecdh['key_gen_ms']/kyber768['key_gen_ms']:.1f}x faster")
print(f"  Encryption: {ecdh['encryption_ms']/kyber768['encryption_ms']:.2f}x")
print(f"  Decryption: {ecdh['decryption_ms']/kyber768['decryption_ms']:.2f}x")

print("\n✓ Comparison complete!")
print("=" * 70)
