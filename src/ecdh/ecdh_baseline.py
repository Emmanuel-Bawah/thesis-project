#!/usr/bin/env python3
"""
ECDH-P256 + AES-256-GCM Baseline System
Elliptic Curve Baseline for Comparison
"""

import json
import time
import base64
from typing import Tuple, Dict
from datetime import datetime

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import psutil


class ECDHBaseline:
    """ECDH-P256 + AES-256-GCM system"""
    
    def __init__(self):
        self.curve = ec.SECP256R1()
        self.symmetric_key_size = 32
        self.nonce_size = 12
        self.metrics = {
            'key_generation_time': [],
            'encryption_time': [],
            'decryption_time': [],
            'memory_usage': []
        }
        print("✓ Initialized ECDH-P256 + AES-256-GCM baseline")
    
    def generate_keypair(self) -> Tuple[bytes, bytes]:
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        private_key = ec.generate_private_key(self.curve)
        public_key = private_key.public_key()
        
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        key_gen_time = (end_time - start_time) * 1000
        memory_used = end_memory - start_memory
        
        self.metrics['key_generation_time'].append(key_gen_time)
        self.metrics['memory_usage'].append(memory_used)
        
        print(f"✓ ECDH keypair generated in {key_gen_time:.2f} ms")
        return public_key_bytes, private_key_bytes
    
    def encrypt(self, plaintext: bytes, public_key_bytes: bytes) -> Dict:
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        # Generate ephemeral key pair
        ephemeral_private = ec.generate_private_key(self.curve)
        ephemeral_public = ephemeral_private.public_key()
        
        # Load recipient's public key
        recipient_public = serialization.load_pem_public_key(public_key_bytes)
        
        # Perform ECDH
        shared_secret = ephemeral_private.exchange(ec.ECDH(), recipient_public)
        
        # Derive AES key from shared secret
        aes_key = HKDF(
            algorithm=hashes.SHA256(),
            length=self.symmetric_key_size,
            salt=None,
            info=b'handshake data'
        ).derive(shared_secret)
        
        # Encrypt with AES-256-GCM
        nonce = get_random_bytes(self.nonce_size)
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        
        # Export ephemeral public key
        ephemeral_public_bytes = ephemeral_public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        encryption_time = (end_time - start_time) * 1000
        memory_used = end_memory - start_memory
        
        self.metrics['encryption_time'].append(encryption_time)
        self.metrics['memory_usage'].append(memory_used)
        
        encrypted_package = {
            'ephemeral_public_key': base64.b64encode(ephemeral_public_bytes).decode('utf-8'),
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'nonce': base64.b64encode(nonce).decode('utf-8'),
            'tag': base64.b64encode(tag).decode('utf-8'),
            'algorithm': 'ECDH-P256+AES-256-GCM',
            'timestamp': datetime.now().isoformat(),
            'encryption_time_ms': round(encryption_time, 2),
            'data_size_bytes': len(plaintext)
        }
        
        print(f"✓ Encrypted {len(plaintext)} bytes in {encryption_time:.2f} ms")
        return encrypted_package
    
    def decrypt(self, encrypted_package: Dict, private_key_bytes: bytes) -> bytes:
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        # Extract components
        ephemeral_public_bytes = base64.b64decode(encrypted_package['ephemeral_public_key'])
        ciphertext = base64.b64decode(encrypted_package['ciphertext'])
        nonce = base64.b64decode(encrypted_package['nonce'])
        tag = base64.b64decode(encrypted_package['tag'])
        
        # Load keys
        private_key = serialization.load_pem_private_key(private_key_bytes, password=None)
        ephemeral_public = serialization.load_pem_public_key(ephemeral_public_bytes)
        
        # Perform ECDH
        shared_secret = private_key.exchange(ec.ECDH(), ephemeral_public)
        
        # Derive AES key
        aes_key = HKDF(
            algorithm=hashes.SHA256(),
            length=self.symmetric_key_size,
            salt=None,
            info=b'handshake data'
        ).derive(shared_secret)
        
        # Decrypt with AES-256-GCM
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        decryption_time = (end_time - start_time) * 1000
        memory_used = end_memory - start_memory
        
        self.metrics['decryption_time'].append(decryption_time)
        self.metrics['memory_usage'].append(memory_used)
        
        print(f"✓ Decrypted {len(plaintext)} bytes in {decryption_time:.2f} ms")
        return plaintext
    
    def get_performance_metrics(self) -> Dict:
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
        metrics = self.get_performance_metrics()
        print("\n" + "=" * 60)
        print("ECDH-P256 PERFORMANCE METRICS (ARM64)")
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
    print("\n" + "=" * 60)
    print("ECDH-P256 + AES-256-GCM BASELINE TEST")
    print("Architecture: ARM64 (AWS t4g.micro)")
    print("=" * 60)
    print()
    
    crypto = ECDHBaseline()
    
    print("Step 1: Generating ECDH-P256 keypair...")
    public_key, private_key = crypto.generate_keypair()
    print(f"  Public key:  {len(public_key)} bytes")
    print(f"  Private key: {len(private_key)} bytes")
    print()
    
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
    print()
    
    print("Step 3: Encrypting...")
    encrypted = crypto.encrypt(plaintext, public_key)
    print()
    
    print("Step 4: Decrypting...")
    decrypted = crypto.decrypt(encrypted, private_key)
    decrypted_data = json.loads(decrypted.decode('utf-8'))
    print()
    
    print("Step 5: Verification...")
    if transaction == decrypted_data:
        print("  ✓ SUCCESS!")
    else:
        print("  ✗ ERROR!")
    print()
    
    crypto.print_metrics()
    
    print("\n✓ ECDH-P256 baseline test complete!")
    print("=" * 60)
    
    return crypto


if __name__ == '__main__':
    try:
        test_system()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
