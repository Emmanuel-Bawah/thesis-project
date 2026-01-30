#!/usr/bin/env python3
"""
Kyber-768 + AES-256-GCM Hybrid Encryption System
MSC Thesis: Post-Quantum E-Commerce Encryption on ARM
"""

import os
import json
import time
import base64
from typing import Tuple, Dict
from datetime import datetime

import oqs
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import psutil

class Kyber768HybridEncryption:
    """Hybrid encryption: Kyber-768 + AES-256-GCM"""
    
    def __init__(self):
        self.kem_algorithm = "Kyber768"
        self.symmetric_key_size = 32  # AES-256
        self.nonce_size = 12  # GCM
        self.metrics = {
            'key_generation_time': [],
            'encryption_time': [],
            'decryption_time': [],
            'memory_usage': []
        }
        print(f"✓ Initialized {self.kem_algorithm} + AES-256-GCM system")
    
    def generate_keypair(self) -> Tuple[bytes, bytes]:
        """Generate Kyber-768 keypair"""
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        kem = oqs.KeyEncapsulation(self.kem_algorithm)
        public_key = kem.generate_keypair()
        private_key = kem.export_secret_key()
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        key_gen_time = (end_time - start_time) * 1000
        memory_used = end_memory - start_memory
        
        self.metrics['key_generation_time'].append(key_gen_time)
        self.metrics['memory_usage'].append(memory_used)
        
        print(f"✓ Keypair generated in {key_gen_time:.2f} ms")
        return public_key, private_key
    
    def encrypt(self, plaintext: bytes, public_key: bytes) -> Dict:
        """Encrypt with Kyber-768 + AES-256-GCM"""
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        # Kyber encapsulation
        kem = oqs.KeyEncapsulation(self.kem_algorithm)
        ciphertext_kem, shared_secret = kem.encap_secret(public_key)
        
        # AES-256 encryption
        aes_key = shared_secret[:self.symmetric_key_size]
        nonce = get_random_bytes(self.nonce_size)
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
        ciphertext_aes, tag = cipher.encrypt_and_digest(plaintext)
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        encryption_time = (end_time - start_time) * 1000
        memory_used = end_memory - start_memory
        
        self.metrics['encryption_time'].append(encryption_time)
        self.metrics['memory_usage'].append(memory_used)
        
        encrypted_package = {
            'ciphertext_kem': base64.b64encode(ciphertext_kem).decode('utf-8'),
            'ciphertext_aes': base64.b64encode(ciphertext_aes).decode('utf-8'),
            'nonce': base64.b64encode(nonce).decode('utf-8'),
            'tag': base64.b64encode(tag).decode('utf-8'),
            'algorithm': 'Kyber768+AES-256-GCM',
            'timestamp': datetime.now().isoformat(),
            'encryption_time_ms': round(encryption_time, 2),
            'data_size_bytes': len(plaintext)
        }
        
        print(f"✓ Encrypted {len(plaintext)} bytes in {encryption_time:.2f} ms")
        return encrypted_package
    
    def decrypt(self, encrypted_package: Dict, private_key: bytes) -> bytes:
        """Decrypt with Kyber-768 + AES-256-GCM"""
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        # Extract components
        ciphertext_kem = base64.b64decode(encrypted_package['ciphertext_kem'])
        ciphertext_aes = base64.b64decode(encrypted_package['ciphertext_aes'])
        nonce = base64.b64decode(encrypted_package['nonce'])
        tag = base64.b64decode(encrypted_package['tag'])
        
        # Kyber decapsulation
        kem = oqs.KeyEncapsulation(self.kem_algorithm, secret_key=private_key)
        shared_secret = kem.decap_secret(ciphertext_kem)
        
        # AES-256 decryption
        aes_key = shared_secret[:self.symmetric_key_size]
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext_aes, tag)
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        decryption_time = (end_time - start_time) * 1000
        memory_used = end_memory - start_memory
        
        self.metrics['decryption_time'].append(decryption_time)
        self.metrics['memory_usage'].append(memory_used)
        
        print(f"✓ Decrypted {len(plaintext)} bytes in {decryption_time:.2f} ms")
        return plaintext
    
    def get_performance_metrics(self) -> Dict:
        """Get performance statistics"""
        def calc_stats(values):
            if not values:
                return {'mean': 0, 'min': 0, 'max': 0, 'count': 0}
            return {
                'mean': round(sum(values) / len(values), 2),
                'min': round(min(values), 2),
                'max': round(max(values), 2),
                'count': len(values)
            }
        
        return {
            'key_generation': calc_stats(self.metrics['key_generation_time']),
            'encryption': calc_stats(self.metrics['encryption_time']),
            'decryption': calc_stats(self.metrics['decryption_time']),
            'memory_usage': calc_stats(self.metrics['memory_usage'])
        }
    
    def print_metrics(self):
        """Print performance metrics"""
        metrics = self.get_performance_metrics()
        print("\n" + "=" * 60)
        print("PERFORMANCE METRICS (ARM64)")
        print("=" * 60)
        for operation, stats in metrics.items():
            if stats['count'] > 0:
                print(f"\n{operation.replace('_', ' ').title()}:")
                print(f"  Mean: {stats['mean']:.2f} ms")
                print(f"  Min:  {stats['min']:.2f} ms")
                print(f"  Max:  {stats['max']:.2f} ms")
                print(f"  Runs: {stats['count']}")
        print("=" * 60)


def test_system():
    """Test the Kyber-768 system with e-commerce transaction"""
    print("\n" + "=" * 60)
    print("KYBER-768 + AES-256-GCM HYBRID SYSTEM TEST")
    print("Architecture: ARM64 (AWS t4g.micro)")
    print("=" * 60)
    print()
    
    crypto = Kyber768HybridEncryption()
    
    # Generate keypair
    print("Step 1: Generating keypair...")
    public_key, private_key = crypto.generate_keypair()
    print(f"  Public key:  {len(public_key)} bytes")
    print(f"  Private key: {len(private_key)} bytes")
    print()
    
    # Create transaction
    print("Step 2: Creating e-commerce transaction...")
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
    print(f"  Transaction: {len(plaintext)} bytes")
    print(f"  Data: {transaction}")
    print()
    
    # Encrypt
    print("Step 3: Encrypting transaction...")
    encrypted = crypto.encrypt(plaintext, public_key)
    print(f"  Encrypted package: ~{len(json.dumps(encrypted))} bytes")
    print()
    
    # Decrypt
    print("Step 4: Decrypting transaction...")
    decrypted = crypto.decrypt(encrypted, private_key)
    decrypted_data = json.loads(decrypted.decode('utf-8'))
    print(f"  Decrypted: {decrypted_data}")
    print()
    
    # Verify
    print("Step 5: Verification...")
    if transaction == decrypted_data:
        print("  ✓ SUCCESS: Data integrity verified!")
    else:
        print("  ✗ ERROR: Data mismatch!")
    print()
    
    # Metrics
    crypto.print_metrics()
    
    print("\n✓ Kyber-768 system test complete!")
    print("=" * 60)
    
    return crypto


if __name__ == '__main__':
    try:
        test_system()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
