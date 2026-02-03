#!/usr/bin/env python3
"""
Adaptive Post-Quantum Encryption Selector
Intelligently selects between Kyber-768 and Kyber-512 based on:
- Device constraints (RAM)
- Network conditions
- Transaction security requirements

NOTE: ONLY selects post-quantum algorithms (no ECDH/RSA)
"""

import sys
sys.path.insert(0, '/home/ubuntu/thesis-project/src/kyber768')
sys.path.insert(0, '/home/ubuntu/thesis-project/src/kyber512')

from kyber768_system import Kyber768HybridEncryption
from kyber512_baseline import Kyber512Baseline


class AdaptivePostQuantumSelector:
    """
    Adaptive selector for post-quantum encryption.
    Chooses between Kyber-768 (NIST Level 3) and Kyber-512 (NIST Level 1)
    based on device, network, and transaction context.
    
    Selection Strategy:
    1. High-value transactions (≥$100): Kyber-768 (maximum security - Level 3)
    2. Low-end devices (≤2GB RAM): Kyber-512 (lighter, Level 1)
    3. Poor network + constrained device: Kyber-512 (optimized for conditions)
    4. Default: Kyber-768 (optimal balance)
    """
    
    # Device RAM thresholds (MB)
    LOW_END_RAM = 2048      # 2GB
    MID_RANGE_RAM = 4096    # 4GB
    
    # Transaction value thresholds (USD)
    HIGH_VALUE = 100.0
    
    # Network quality scores
    NETWORK_SCORES = {
        '2G': 1,  # Poor
        '3G': 2,  # Moderate
        '4G': 3   # Good
    }
    
    def __init__(self):
        self.systems = {
            'kyber768': Kyber768HybridEncryption(),
            'kyber512': Kyber512Baseline(),
        }
        
        self.selection_count = {
            'kyber768': 0,
            'kyber512': 0,
        }
        
        print("✓ Adaptive Post-Quantum Selector initialized (Kyber-768 & Kyber-512)")
    
    def select_algorithm(self, device_ram_mb, network_type, transaction_amount):
        """
        Select optimal post-quantum algorithm based on context.
        
        Args:
            device_ram_mb: Device RAM in MB
            network_type: '2G', '3G', or '4G'
            transaction_amount: Transaction value in USD
            
        Returns:
            Tuple of (algorithm_name, system_instance, reason)
        """
        
        # Rule 1: High-value transactions ALWAYS use Kyber-768 (NIST Level 3)
        if transaction_amount >= self.HIGH_VALUE:
            reason = f"High-value (${transaction_amount:.2f}) requires maximum quantum security (Level 3)"
            self.selection_count['kyber768'] += 1
            return 'kyber768', self.systems['kyber768'], reason
        
        # Rule 2: Low-end devices use Kyber-512 (lighter, still quantum-safe)
        if device_ram_mb <= self.LOW_END_RAM:
            reason = f"Low-end device ({device_ram_mb}MB RAM) optimized with Kyber-512 (Level 1)"
            self.selection_count['kyber512'] += 1
            return 'kyber512', self.systems['kyber512'], reason
        
        # Rule 3: Mid-range devices on poor network use Kyber-512
        if device_ram_mb <= self.MID_RANGE_RAM and network_type == '2G':
            reason = f"Mid-range device + poor network ({network_type}) → Kyber-512 optimized"
            self.selection_count['kyber512'] += 1
            return 'kyber512', self.systems['kyber512'], reason
        
        # Default: Kyber-768 (optimal for most cases)
        reason = "Standard conditions: Kyber-768 provides optimal security/performance balance"
        self.selection_count['kyber768'] += 1
        return 'kyber768', self.systems['kyber768'], reason
    
    def get_selection_statistics(self):
        """Get statistics on algorithm selections."""
        total = sum(self.selection_count.values())
        if total == 0:
            return {}
        
        return {
            algo: {
                'count': count,
                'percentage': (count / total) * 100
            }
            for algo, count in self.selection_count.items()
        }
    
    def print_selection_summary(self):
        """Print summary of algorithm selections."""
        stats = self.get_selection_statistics()
        total = sum(self.selection_count.values())
        
        print("\n" + "="*60)
        print("ADAPTIVE POST-QUANTUM SELECTION SUMMARY")
        print("="*60)
        print(f"Total selections: {total}")
        print()
        
        for algo, data in sorted(stats.items(), key=lambda x: x[1]['count'], reverse=True):
            if data['count'] > 0:
                level = "NIST Level 3" if algo == 'kyber768' else "NIST Level 1"
                print(f"{algo:12s}: {data['count']:4d} times ({data['percentage']:5.1f}%) - {level}")
        
        print("="*60)
        print("✓ All selections are quantum-resistant (post-quantum secure)")
        print("="*60)


def test_adaptive_selector():
    """Test the adaptive post-quantum selector."""
    print("\n" + "="*60)
    print("TESTING ADAPTIVE POST-QUANTUM SELECTOR")
    print("="*60)
    print()
    
    selector = AdaptivePostQuantumSelector()
    
    # Test scenarios covering African mobile commerce
    scenarios = [
        # (device_ram, network, amount, description)
        (1536, '2G', 150.0, "High-value on low-end device (rural farmer)"),
        (1536, '2G', 5.0, "Low-value on low-end + poor network (airtime)"),
        (4096, '4G', 5.0, "Low-value on high-end + good network (coffee)"),
        (4096, '4G', 50.0, "Medium-value on high-end device (groceries)"),
        (2048, '3G', 25.0, "Medium-value on mid-range device (utilities)"),
        (6144, '4G', 200.0, "High-value on high-end device (rent)"),
        (3584, '2G', 75.0, "Medium-high on mid-range + 2G (merchant)"),
        (1792, '3G', 15.0, "Low-medium on low-end + 3G (transport)"),
    ]
    
    print("Testing post-quantum selection logic:\n")
    
    for device_ram, network, amount, description in scenarios:
        algo, system, reason = selector.select_algorithm(device_ram, network, amount)
        security_level = "NIST Level 3 (192-bit)" if algo == 'kyber768' else "NIST Level 1 (128-bit)"
        
        print(f"Scenario: {description}")
        print(f"  Context: {device_ram}MB RAM, {network}, ${amount:.2f}")
        print(f"  Selected: {algo} ({security_level})")
        print(f"  Reason: {reason}")
        print()
    
    selector.print_selection_summary()
    
    print("\n✓ Adaptive post-quantum selector test complete!")
    print("✓ System is fully quantum-resistant (no classical crypto)")


if __name__ == '__main__':
    test_adaptive_selector()
